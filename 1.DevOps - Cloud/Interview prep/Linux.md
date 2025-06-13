
## 🐧 Linux for DevOps – Interview Questions & Answers

### 🔹 **1. Linux Basics**

**Q1. What is Linux?**  
A: Linux is an open-source Unix-like operating system kernel used to run applications on servers, desktops, embedded devices, and cloud systems.

**Q2. Difference between Linux and Unix?**  
A: Unix is proprietary; Linux is open-source and widely supported across modern platforms.

**Q3. How to check the current Linux version?**  
A: Use `uname -a`, `cat /etc/os-release`, or `lsb_release -a`.

---

### 🔹 **2. File System & Navigation**

**Q4. What is the root directory in Linux?**  
A: The top-level directory: `/`. Everything starts from here.

**Q5. Basic navigation commands?**  
A:

- `cd` – Change directory
- `pwd` – Show current directory
- `ls` – List files
- `tree` – Show directory structure

**Q6. What is the difference between absolute and relative paths?**  
A: Absolute starts from `/`, relative starts from current directory.

---

### 🔹 **3. File Permissions & Ownership**

**Q7. How to change file permissions?**  
A: Use `chmod`.  
Example: `chmod 755 file.sh` (rwxr-xr-x)

**Q8. How to change file ownership?**  
A: Use `chown`.  
Example: `chown user:group file.txt`

**Q9. What does `ls -l` show?**  
A: Permissions, owner, group, size, and last modified date.

---

### 🔹 **4. Process Management**

**Q10. How to view running processes?**  
A: `ps aux`, `top`, or `htop`.

**Q11. How to kill a process?**  
A: `kill <PID>` or `kill -9 <PID>` (forcefully)

**Q12. What is the difference between `kill` and `pkill`?**  
A: `kill` uses PID, `pkill` uses process name.

---

### 🔹 **5. Package Management**

**Q13. How to install packages in Debian/Ubuntu?**  
A: `sudo apt update && sudo apt install <package>`

**Q14. How to install packages in RHEL/CentOS?**  
A: `sudo yum install <package>` or `dnf` for newer systems.

**Q15. How to find installed packages?**  
A: `dpkg -l` or `rpm -qa`

---

### 🔹 **6. User & Group Management**

**Q16. How to create a user?**  
A: `sudo useradd -m username`  
Then set password: `passwd username`

**Q17. Add user to a group?**  
A: `sudo usermod -aG groupname username`

**Q18. Check group memberships?**  
A: `groups username`

---

### 🔹 **7. File Management & Searching**

**Q19. Copy, move, delete files?**  
A:

- `cp source dest`
- `mv source dest`
- `rm file`

**Q20. How to find a file?**  
A: `find / -name filename` or `locate filename`

**Q21. How to search inside files?**  
A: `grep 'pattern' file.txt`

---

### 🔹 **8. Networking Commands**

**Q22. How to check IP address?**  
A: `ip a` or `ifconfig` (older)

**Q23. How to test network connectivity?**  
A: `ping`, `traceroute`, `curl`, `telnet`, `nc`

**Q24. Open ports?**  
A: `netstat -tuln` or `ss -tuln`

---

### 🔹 **9. Disk & Memory Monitoring**

**Q25. Disk usage command?**  
A: `df -h` for disks, `du -sh *` for folders.

**Q26. Check memory and CPU usage?**  
A: `free -h`, `top`, `htop`, `vmstat`

**Q27. Check inode usage?**  
A: `df -i`

---

### 🔹 **10. Scheduled Jobs (Cron)**

**Q28. What is cron?**  
A: A daemon to run scheduled jobs.

**Q29. How to view/edit crontab?**  
A:

- View: `crontab -l`
    
- Edit: `crontab -e`
    

**Q30. Sample cron syntax?**  
A: `0 2 * * * /home/user/backup.sh` → runs every day at 2 AM.

---

### 🔹 **11. Log Management**

**Q31. How to view logs?**  
A: `cat`, `less`, `tail`, or `journalctl` (for systemd)

**Q32. Follow logs in real-time?**  
A: `tail -f /var/log/syslog`

---

### 🔹 **12. File Compression & Archiving**

**Q33. How to zip/unzip files?**  
A:

- `tar -czf file.tar.gz folder/`
- `tar -xzf file.tar.gz`

**Q34. Check contents of a tar file?**  
A: `tar -tf file.tar.gz`

---

### 🔹 **13. Shell Scripting Basics**

**Q35. How to make a script executable?**  
A: `chmod +x script.sh`

**Q36. How to run a shell script?**  
A: `./script.sh` or `bash script.sh`

**Q37. What is shebang (`#!/bin/bash`)?**  
A: Specifies the interpreter to run the script.

---

### 🔹 **14. Systemd & Services**

**Q38. Check service status?**  
A: `systemctl status nginx`

**Q39. Start/stop/restart a service?**  
A:

- `systemctl start nginx`
    
- `systemctl stop nginx`
    
- `systemctl restart nginx`
    

**Q40. Enable a service on boot?**  
A: `systemctl enable nginx`

---

## ✅ BONUS: Most Common Real Interview Questions

- What are runlevels or systemd targets?
- What happens when you run `sudo`?
- What is a zombie process?
- How to secure a Linux server (basic hardening)?
- How to debug high CPU usage?

---


## 🧠 Intermediate Linux Interview Questions (with Answers)

---

### 🔹 1. **What is the difference between a process and a thread?**

- **Process**: An independent unit with its own memory space.
- **Thread**: A lightweight sub-part of a process that shares memory with other threads of the same process.

---

### 🔹 2. **How do you check open file descriptors and their limits?**

- Per-process: `ls /proc/<pid>/fd`
- Limit: `ulimit -n`
- System-wide: `cat /proc/sys/fs/file-max`

---

### 🔹 3. **What is a zombie process? How do you find and kill it?**
A zombie process is dead but its entry remains in the process table until its parent reads its exit status.

- Find: `ps aux | grep Z`
- Kill parent process if needed.

---

### 🔹 4. **What’s the difference between hard link and soft (symbolic) link?**

- **Hard link**: Points directly to the inode. File continues to exist even if the original is deleted.
- **Soft link**: Shortcut to the file path. Breaks if original file is deleted.

---

### 🔹 5. **Explain nice and renice commands.**

- `nice`: Starts a process with a priority value (lower = higher priority).
- `renice`: Changes the priority of a running process.

```bash
nice -n 10 myscript.sh
renice -n -5 -p 1234
```

---

### 🔹 6. **How do you debug a system that is running out of memory?**

**A:**

- Check memory usage: `free -h`, `top`, `vmstat`, `htop`
- Check logs: `/var/log/syslog`, `dmesg`
- Identify heavy processes: `ps aux --sort=-%mem | head`

---

### 🔹 7. **How does `rsync` work?**
Efficient file sync tool that transfers only the differences using the delta algorithm.

```bash
rsync -avz source/ user@remote:/path/
```

---

### 🔹 8. **How to find which process is using a particular port?**

```bash
sudo lsof -i :8080
sudo netstat -tulnp | grep 8080
```

---

### 🔹 9. **What is SELinux/AppArmor?**
Linux security modules for **Mandatory Access Control**:

- **SELinux**: RedHat/CentOS
- **AppArmor**: Ubuntu/Debian  
    They restrict programs' access beyond file permissions.

---

### 🔹 10. **Explain runlevels (or systemd targets).**

- Runlevels are modes like:
    - 0 = Halt
    - 1 = Single-user
    - 3 = Multi-user
    - 5 = GUI
    - 6 = Reboot


In **systemd**:

```bash
systemctl get-default
systemctl isolate multi-user.target
```

---

### 🔹 11. **How to check disk I/O performance?**

**A:**

- `iostat -x 1`
- `iotop` (for per-process I/O)
- `df -h` (disk usage)
- `du -sh *` (space used by directories)

---

### 🔹 12. **What is the difference between /etc/fstab and mount command?**

**A:**

- `fstab`: Config file for mounting filesystems automatically at boot.
- `mount`: Manual command to mount filesystems.

---

### 🔹 13. **How to debug system boot issues?**

**A:**

- Use `journalctl -xb`
- Look into `/var/log/boot.log`
- Use recovery mode or rescue target
---

### 🔹 14. **How do cron and anacron differ?**

- `cron`: Runs jobs based on time — skips missed jobs (e.g., system off).
- `anacron`: Runs missed jobs once system is back up — good for laptops/desktops.

---

### 🔹 15. **What is `/proc` and why is it useful?**

Virtual filesystem that provides real-time system info.  
Useful for process info (`/proc/PID`), CPU/mem (`/proc/meminfo`, `/proc/cpuinfo`), mounts, etc.

---

### 🔹 16. **What is `strace` and when would you use it?**
`strace` traces system calls and signals used by a process — useful for debugging binaries or startup errors.

```bash
strace ./app
```

---

### 🔹 17. **How do you check system resource limits?**

Use `ulimit -a` (per-user)  
System-wide: `/etc/security/limits.conf`

---

### 🔹 18. **What is sticky bit?**

Special permission bit: allows only the file **owner** or **root** to delete files in a shared directory (e.g., `/tmp`).

```bash
chmod +t /shared_folder
```

---

### 🔹 19. **What is the difference between grep, egrep, and fgrep?**

- `grep`: Basic regex
- `egrep`: Extended regex (supports `+`, `?`, etc.)
- `fgrep`: Fixed strings (no regex)

---

### 🔹 20. **How to limit CPU and memory usage of a process?**

- Use `ulimit` in shell
- Or control groups (`cgroups`) for containers/system-wide control

---
