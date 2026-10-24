import test from "node:test"
import assert from "node:assert/strict"
import crypto from "node:crypto"
import { generateKeyPair, SignJWT } from "jose"
import { googleLoginConfiguration, createGoogleLogin } from "./google-login.mjs"
import { createDashboard } from "./server.mjs"
import http from "node:http"

const config = {
  origin: "https://workspace.example.com",
  host: "workspace.example.com",
  owner: "owner@example.com",
  redirect: "https://workspace.example.com/auth/callback",
  clientId: "test-client",
  clientSecret: "test-secret",
}
const { privateKey, publicKey } = await generateKeyPair("RS256")
const request = (cookie = "") => ({ method: "GET", headers: { cookie } })
const url = (path) => new URL(path, config.origin)
function harness(overrides = {}) {
  let claims,
    calls = 0,
    exchange
  const auth = createGoogleLogin(config, {
    keys: publicKey,
    fetchImpl: async (_url, options) => {
      calls++
      exchange = options.body
      const token = await new SignJWT({
        email: config.owner,
        email_verified: true,
        nonce: claims.nonce,
        ...overrides,
      })
        .setProtectedHeader({ alg: "RS256" })
        .setSubject("owner-subject")
        .setIssuer("https://accounts.google.com")
        .setAudience(overrides.aud || config.clientId)
        .setIssuedAt()
        .setExpirationTime(overrides.exp || "5m")
        .sign(privateKey)
      return { ok: true, json: async () => ({ id_token: token }) }
    },
  })
  return {
    auth,
    get calls() {
      return calls
    },
    get exchange() {
      return exchange
    },
    async start() {
      const login = await auth.handle(request(), url("/auth/login"))
      const target = new URL(login.location)
      claims = Object.fromEntries(target.searchParams)
      return { login, target, state: claims.state, cookie: login.cookies[0].split(";")[0] }
    },
  }
}

test("online configuration fails closed and requires the exact web callback", () => {
  assert.equal(googleLoginConfiguration({}), null)
  assert.throws(() => googleLoginConfiguration({ VAULT_DASHBOARD_OWNER: config.owner }))
  const env = {
    VAULT_DASHBOARD_ORIGIN: config.origin,
    VAULT_GOOGLE_WEB_CLIENT: "unused",
    VAULT_DASHBOARD_OWNER: config.owner,
  }
  const client = {
    web: {
      client_id: config.clientId,
      client_secret: config.clientSecret,
      redirect_uris: [config.redirect],
    },
  }
  assert.deepEqual(googleLoginConfiguration(env, client), config)
  assert.throws(() =>
    googleLoginConfiguration(
      { ...env, VAULT_DASHBOARD_ORIGIN: "http://workspace.example.com" },
      client,
    ),
  )
  assert.throws(() => googleLoginConfiguration(env, { installed: client.web }))
  assert.throws(() => googleLoginConfiguration(env, { web: { ...client.web, redirect_uris: [] } }))
})

test("owner sign-in verifies identity and PKCE, creates a secure session, and supports logout", async () => {
  const h = harness(),
    flow = await h.start()
  assert.equal(flow.target.origin, "https://accounts.google.com")
  assert.equal(flow.target.searchParams.get("scope"), "openid email")
  assert.equal(flow.target.searchParams.get("code_challenge_method"), "S256")
  assert.match(flow.login.cookies[0], /HttpOnly; Secure; SameSite=Lax/)
  const result = await h.auth.handle(
    request(flow.cookie),
    url(`/auth/callback?state=${flow.state}&code=test-code`),
  )
  assert.equal(result.status, 302)
  assert.equal(result.location, "/")
  assert.equal(
    crypto.createHash("sha256").update(h.exchange.get("code_verifier")).digest("base64url"),
    flow.target.searchParams.get("code_challenge"),
  )
  const session = result.cookies[0].split(";")[0]
  assert.equal(h.auth.authenticated(request(session)), true)
  h.auth.logout(request(session))
  assert.equal(h.auth.authenticated(request(session)), false)
  assert.equal(
    (
      await h.auth.handle(
        request(flow.cookie),
        url(`/auth/callback?state=${flow.state}&code=test-code`),
      )
    ).status,
    403,
  )
  assert.equal(h.calls, 1)
})

for (const [name, overrides] of Object.entries({
  "other account": { email: "stranger@example.com" },
  "unverified email": { email_verified: false },
  "wrong nonce": { nonce: "wrong" },
  "wrong audience": { aud: "other-client" },
  "expired identity": { exp: 1 },
})) {
  test(`sign-in rejects ${name}`, async () => {
    const h = harness(overrides),
      flow = await h.start()
    const result = await h.auth.handle(
      request(flow.cookie),
      url(`/auth/callback?state=${flow.state}&code=test-code`),
    )
    assert.equal(result.status, 403)
    assert.equal(
      result.cookies.some((c) => c.startsWith("vault_session=")),
      false,
    )
  })
}

test("callback without matching browser state cannot exchange a code", async () => {
  const h = harness(),
    flow = await h.start()
  assert.equal(
    (
      await h.auth.handle(
        request("vault_login=wrong"),
        url(`/auth/callback?state=${flow.state}&code=test-code`),
      )
    ).status,
    403,
  )
  assert.equal(h.calls, 0)
})

test("online HTTP server blocks private data and unknown Host headers before serving anything", async (t) => {
  const app = createDashboard({ login: config })
  await new Promise((resolve) => app.listen(0, "127.0.0.1", resolve))
  t.after(() => new Promise((resolve) => app.close(resolve)))
  const get = (path, host = config.host) =>
    new Promise((resolve, reject) => {
      http
        .get(
          { host: "127.0.0.1", port: app.address().port, path, headers: { Host: host } },
          (res) => {
            let body = ""
            res.on("data", (chunk) => (body += chunk))
            res.on("end", () =>
              resolve({ status: res.statusCode, location: res.headers.location, body }),
            )
          },
        )
        .on("error", reject)
    })
  assert.equal((await get("/")).location, "/auth/login")
  for (const path of [
    "/api/context",
    "/api/overview",
    "/api/search?q=private",
    "/app.js",
    "/private/google/token.json",
  ])
    assert.equal((await get(path)).status, 401)
  assert.equal((await get("/", "attacker.example.com")).status, 403)
})
