
#  Administrator-Side IT Support Automation Scripts

### User Management & Access Control
- User account creation and give access control _(standard and administrator access)_
- Bulk User Account Creation – Creates multiple Active Directory (AD) users.
- Password Expiry Notifier – Sends automated email reminders for expiring passwords.
- Auto-Reset Expired Passwords – Resets passwords and emails new credentials to users.
- Monitor User Login History – Tracks login attempts and failed logins.
- Assign User Permissions & Group Policies – Automates permission assignment.
- Generate AD User Reports – Exports all users, groups, _and their roles to CSV._
---
### System & Performance Monitoring
- Real-Time CPU & Memory Monitoring     
- Disk Space Auto-Cleanup & Alerts – Deletes temp files and warns if space is low.
- Monitor & Restart Stuck Services 
- Scheduled Server Reboots 
- Process Monitor & Auto-Kill High CPU Task
- Monitor Running Applications & Services
- Auto-Optimize Windows Performance
- Automated Event Log Monitoring 
- Check & Report System Uptime
---
### Networking & Connectivity

- Bulk IP & DNS Configuration for Systems – Automates network setup.
- Auto-Detect & Fix Network Issues – Runs network diagnostics and resets settings.
- Check & Restart Network Adapter – Detects failures and auto-restarts adapters.
- Monitor Internet Connection Stability – Logs ping failures and notifies admins.
- Automated Firewall Rules Deployment – Sets security rules across multiple PCs.
- Auto-Switch Between Static & DHCP – Adapts network settings for different locations.
- Wi-Fi SSID Whitelisting – Restricts access to specific corporate Wi-Fi networks.
- Auto-Disable Open/Public Wi-Fi Connections – Improves security for remote users.
- Restart Network Services on Connection Loss – Ensures internet recovery.

---

### Security & Compliance Enforcement
- Automated Windows Update Management – Forces updates on systems.
- Scan & Remove Malware Using Defender – Automates Windows Defender scans.
- Security Patch Deployment Script – Installs latest patches across multiple machines.
- Detect & Block Unauthorized USB Devices – Prevents data leaks.
- Monitor Suspicious Logins & Access Attempts – Detects brute-force attempts.
- Force BitLocker Encryption on New Drives – Ensures disk security compliance.
- Auto-Disable Inactive AD Accounts – Locks accounts with no recent activity.
- Set & Enforce Password Complexity Policies – Applies secure password rules.
- Export Security Audit Reports for Compliance – Generates security summaries.
---

### Software & Patch Management

- Silent Software Installation & Updates – Installs software without user interaction.
- Uninstall Unauthorized Applications – Removes non-approved software.
- Monitor & Auto-Restart Crashed Applications – Ensures service availability.   
- Automatically Update All Installed Software – Checks for outdated versions.
- Reset Default Apps & File Associations – Fixes broken file type mappings.
- Reinstall & Repair Corrupt System Files – Runs `sfc /scannow` and `DISM`.
---

###  Backup & Disaster Recovery

- Automated System Restore Point Creation – Creates restore points before updates.
- Scheduled Backup of Critical Files – Syncs data to an external drive or cloud.
- Auto-Restore Files from Backups – Recovers lost or deleted files.    
- Schedule Full System Image Backups – Creates disk clones for disaster recovery.
---

###  Remote Administration & Automation

- Remote Power On/Off & Restart via PowerShell – Controls multiple machines.
- Remote Lock & Logout for Security Enforcement – Secures unattended PCs.
- Send Messages to Remote Users via PowerShell – Notifies about maintenance.

---
### BSOD & System Crash Handling

- BSOD Log Collector & Crash Dump Analyzer – Saves crash logs for debugging.
- Auto-Detect & Fix Common BSOD Errors – Uses event logs for diagnosis.
- Check & Auto-Update Faulty Drivers – Reduces driver-related crashes.
- Reboot System on Critical Errors – Ensures uptime after failures.
- Scheduled System Health Reports for BSOD Prevention – Proactive monitoring.
