import fs from "node:fs"
import crypto from "node:crypto"
import { createRemoteJWKSet, jwtVerify } from "jose"

const GOOGLE_AUTH = "https://accounts.google.com/o/oauth2/v2/auth"
const GOOGLE_TOKEN = "https://oauth2.googleapis.com/token"
const GOOGLE_KEYS = "https://www.googleapis.com/oauth2/v3/certs"
const SESSION_AGE = 8 * 60 * 60 * 1000
const LOGIN_AGE = 10 * 60 * 1000

export function googleLoginConfiguration(env = process.env, suppliedClient) {
  const values = [
    env.VAULT_DASHBOARD_ORIGIN,
    env.VAULT_GOOGLE_WEB_CLIENT,
    env.VAULT_DASHBOARD_OWNER,
  ]
  if (!values.some(Boolean)) return null
  if (!values.every(Boolean))
    throw new Error("Online workspace requires HTTPS origin, Web OAuth client and owner email")
  const origin = new URL(env.VAULT_DASHBOARD_ORIGIN)
  if (
    origin.protocol !== "https:" ||
    origin.username ||
    origin.password ||
    origin.pathname !== "/" ||
    origin.search ||
    origin.hash
  )
    throw new Error("Workspace origin must be a plain HTTPS origin")
  const owner = env.VAULT_DASHBOARD_OWNER.trim().toLowerCase()
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(owner)) throw new Error("Owner email is invalid")
  const client = (
    suppliedClient || JSON.parse(fs.readFileSync(env.VAULT_GOOGLE_WEB_CLIENT, "utf8"))
  ).web
  const redirect = origin.origin + "/auth/callback"
  if (!client?.client_id || !client?.client_secret || !client.redirect_uris?.includes(redirect))
    throw new Error("Use a Web OAuth client with the workspace callback URL")
  return {
    origin: origin.origin,
    host: origin.host,
    owner,
    redirect,
    clientId: client.client_id,
    clientSecret: client.client_secret,
  }
}

export function createGoogleLogin(config, { fetchImpl = fetch, keys } = {}) {
  const jwks = keys || createRemoteJWKSet(new URL(GOOGLE_KEYS), { timeoutDuration: 5000 })
  const pending = new Map(),
    sessions = new Map()
  const random = () => crypto.randomBytes(32).toString("base64url")
  const cookie = (name, value, maxAge) =>
    `${name}=${value}; Path=/; HttpOnly; Secure; SameSite=Lax; Max-Age=${maxAge}`
  const cookies = (request) =>
    Object.fromEntries(
      (request.headers.cookie || "")
        .split(";")
        .map((part) => part.trim().split("="))
        .filter((pair) => pair.length === 2),
    )
  const prune = () => {
    for (const map of [pending, sessions]) {
      for (const [key, value] of map) if (value.expires <= Date.now()) map.delete(key)
      while (map.size > 128) map.delete(map.keys().next().value)
    }
  }
  const authenticated = (request) => {
    prune()
    return !!sessions.get(cookies(request).vault_session)
  }
  const logout = (request) => {
    sessions.delete(cookies(request).vault_session)
    return cookie("vault_session", "", 0)
  }
  const handle = async (request, url) => {
    if (!["/auth/login", "/auth/callback"].includes(url.pathname)) return null
    if (request.method !== "GET") return { status: 405, body: "Method not supported" }
    prune()
    if (url.pathname === "/auth/login") {
      const state = random(),
        verifier = random(),
        nonce = random()
      pending.set(state, { verifier, nonce, expires: Date.now() + LOGIN_AGE })
      const target = new URL(GOOGLE_AUTH)
      target.search = new URLSearchParams({
        client_id: config.clientId,
        redirect_uri: config.redirect,
        response_type: "code",
        scope: "openid email",
        state,
        nonce,
        prompt: "select_account",
        code_challenge: crypto.createHash("sha256").update(verifier).digest("base64url"),
        code_challenge_method: "S256",
      }).toString()
      return {
        status: 302,
        location: target.href,
        cookies: [cookie("vault_login", state, LOGIN_AGE / 1000)],
      }
    }
    const state = url.searchParams.get("state")
    const transaction = pending.get(state)
    pending.delete(state)
    try {
      if (
        !state ||
        state !== cookies(request).vault_login ||
        !transaction ||
        !url.searchParams.get("code") ||
        url.searchParams.has("error")
      )
        throw new Error("Login state mismatch")
      const response = await fetchImpl(GOOGLE_TOKEN, {
        method: "POST",
        signal: AbortSignal.timeout(15000),
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: new URLSearchParams({
          client_id: config.clientId,
          client_secret: config.clientSecret,
          redirect_uri: config.redirect,
          grant_type: "authorization_code",
          code: url.searchParams.get("code"),
          code_verifier: transaction.verifier,
        }),
      })
      if (!response.ok) throw new Error("Google authorization exchange failed")
      const result = await response.json()
      if (typeof result.id_token !== "string" || result.id_token.length > 20000)
        throw new Error("Missing identity token")
      const { payload } = await jwtVerify(result.id_token, jwks, {
        issuer: ["https://accounts.google.com", "accounts.google.com"],
        audience: config.clientId,
        algorithms: ["RS256"],
        requiredClaims: ["exp", "iat", "sub", "email", "nonce"],
      })
      if (
        (payload.azp && payload.azp !== config.clientId) ||
        payload.nonce !== transaction.nonce ||
        payload.email_verified !== true ||
        typeof payload.email !== "string" ||
        payload.email.toLowerCase() !== config.owner
      )
        throw new Error("This is not the verified workspace owner")
      const session = random()
      sessions.set(session, { expires: Date.now() + SESSION_AGE })
      return {
        status: 302,
        location: "/",
        cookies: [
          cookie("vault_session", session, SESSION_AGE / 1000),
          cookie("vault_login", "", 0),
        ],
      }
    } catch {
      return {
        status: 403,
        cookies: [cookie("vault_login", "", 0)],
        body: '<!doctype html><meta name="viewport" content="width=device-width"><title>Workspace sign-in</title><h1>Sign-in could not be completed</h1><p>Use the Google account configured as the workspace owner.</p><a href="/auth/login">Try Google sign-in again</a>',
      }
    }
  }
  return { handle, authenticated, logout }
}
