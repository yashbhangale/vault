import fs from "node:fs/promises"
import os from "node:os"
import path from "node:path"
import { fileURLToPath } from "node:url"
import { execFileSync } from "node:child_process"

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "../..")
const folder = path.join(os.homedir(), ".config/systemd/user")
const config = path.join(root, "private/dashboard/tunnel.yml")
const binary = path.join(os.homedir(), ".local/bin/cloudflared")
const quote = (value) =>
  '"' + value.replaceAll("\\", "\\\\").replaceAll('"', '\\"').replaceAll("%", "%%") + '"'
const command = process.argv[2] || "status"
const unitName = "vault-workspace-tunnel.service"
if (command === "install") {
  await fs.access(config)
  await fs.access(path.join(root, "private/dashboard/online.env"))
  await fs.access(binary)
  execFileSync(binary, ["tunnel", "--config", config, "ingress", "validate"], { stdio: "inherit" })
  await fs.mkdir(folder, { recursive: true })
  await fs.writeFile(
    path.join(folder, unitName),
    `[Unit]\nDescription=Owner-only vault workspace HTTPS tunnel\nAfter=network-online.target vault-dashboard.service\nWants=network-online.target vault-dashboard.service\n\n[Service]\nType=simple\nExecStart=${quote(binary)} --no-autoupdate tunnel --config ${quote(config)} run\nRestart=always\nRestartSec=10\nUMask=0077\n\n[Install]\nWantedBy=default.target\n`,
    { mode: 0o600 },
  )
  execFileSync("systemctl", ["--user", "daemon-reload"], { stdio: "inherit" })
  execFileSync("systemctl", ["--user", "enable", "--now", unitName], { stdio: "inherit" })
  console.log("Workspace tunnel enabled. This laptop must stay awake and connected.")
} else if (command === "disable")
  execFileSync("systemctl", ["--user", "disable", "--now", unitName], { stdio: "inherit" })
else if (command === "status")
  execFileSync("systemctl", ["--user", "status", unitName, "--no-pager"], { stdio: "inherit" })
else throw new Error("Use install, status, or disable")
