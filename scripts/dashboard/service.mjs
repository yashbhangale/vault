import fs from "node:fs/promises"
import os from "node:os"
import path from "node:path"
import { fileURLToPath } from "node:url"
import { execFileSync } from "node:child_process"

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "../..")
const folder = path.join(os.homedir(), ".config/systemd/user")
const quote = (value) =>
  '"' + value.replaceAll("\\", "\\\\").replaceAll('"', '\\"').replaceAll("%", "%%") + '"'
const command = process.argv[2] || "status"
if (command === "install") {
  await fs.mkdir(folder, { recursive: true })
  const unit =
    "[Unit]\nDescription=Local vault and Quartz workspace\n\n[Service]\nType=simple\nExecStart=" +
    quote(process.execPath) +
    " " +
    quote(path.join(root, "scripts/dashboard/server.mjs")) +
    "\nRestart=on-failure\nRestartSec=5\nUMask=0077\n\n[Install]\nWantedBy=default.target\n"
  await fs.writeFile(path.join(folder, "vault-dashboard.service"), unit, { mode: 0o600 })
  execFileSync("systemctl", ["--user", "daemon-reload"], { stdio: "inherit" })
  execFileSync("systemctl", ["--user", "enable", "--now", "vault-dashboard.service"], {
    stdio: "inherit",
  })
  console.log("Local workspace starts with your user services: http://127.0.0.1:4173/")
} else if (command === "disable")
  execFileSync("systemctl", ["--user", "disable", "--now", "vault-dashboard.service"], {
    stdio: "inherit",
  })
else if (command === "status")
  execFileSync("systemctl", ["--user", "status", "vault-dashboard.service", "--no-pager"], {
    stdio: "inherit",
  })
else {
  console.error("Use install, status, or disable")
  process.exitCode = 1
}
