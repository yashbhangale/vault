---
title: Filesystem & Storage
tags: [devops---cloud, linux]
---

#  1. What is Filesystem in Linux?

A **filesystem** defines **how data is stored, organized, and accessed** on storage devices.

👉 Think:

- Disk = raw storage

- Filesystem = structure + rules to store files


### Examples:

- `ext4` (most common in Linux)

- `xfs` (used in enterprise, high performance)
- `btrfs` (advanced features like snapshots)

- `tmpfs` (in-memory filesystem)


---

# 2. Linux Storage Stack (VERY IMPORTANT)

In interviews, always explain this **layered architecture** 👇

```
Application
   ↓
Filesystem (ext4, xfs)
   ↓
VFS (Virtual File System)
   ↓
Block Layer
   ↓
Device Drivers
   ↓
Physical Disk (HDD/SSD/NVMe)
```

### 🔥 Key Points:

- **VFS (Virtual File System)** → abstraction layer  
→ allows Linux to support multiple filesystems

- Apps don’t care if it's ext4, xfs, NFS, etc.


👉 Interview line:

> “Linux uses VFS to provide a unified interface across different filesystem types.”

---

# 🗂️ 3. Types of Filesystems (Important)

### 🔹 Local Filesystems

- `ext4` → default, journaling, stable

- `xfs` → high performance, large files

- `btrfs` → snapshots, compression


### 🔹 Network Filesystems

- `NFS` → share storage across servers

- `SMB/CIFS` → Windows-compatible sharing


### 🔹 Virtual / Special

- `procfs` → process info (`/proc`)

- `sysfs` → kernel/device info (`/sys`)

- `tmpfs` → RAM-based


---

# 📁 4. Linux Directory Structure (FHS)

Very common question.

|Directory|Purpose|
|---|---|
|`/`|Root|
|`/home`|User data|
|`/var`|Logs, dynamic data|
|`/etc`|Config files|
|`/bin`, `/usr/bin`|Binaries|
|`/dev`|Devices|
|`/proc`|Process info|

👉 Interview tip:

> “Linux follows FHS (Filesystem Hierarchy Standard) to maintain consistency.”

---

# 💽 5. Storage Concepts (CORE DEVOPS PART)

## 🔹 Partitioning

Splitting disk into parts.

Commands:

```bash
fdisk
parted
lsblk
```

---

## 🔹 Mounting

Linux doesn’t auto-use disks → you must mount.

```bash
mount /dev/sdb1 /mnt/data
```

Persistent mount:

```bash
/etc/fstab
```

👉 Critical interview point:

> “Everything in Linux is mounted under root `/` — unlike Windows drives.”

---

## 🔹 Inodes (VERY IMPORTANT)

Each file has an **inode** containing:

- metadata

- permissions

- size

- pointers to data blocks


👉 NOT filename (that’s stored in directory)

Check:

```bash
ls -i
df -i
```

👉 Interview trap:

> Disk can have free space but still fail if inodes are exhausted.

---

## 🔹 Journaling

Used in `ext4`, `xfs`

👉 Prevents corruption during crashes  
→ logs changes before writing

---

# ⚙️ 6. LVM (Logical Volume Manager) 🔥🔥

**VERY IMPORTANT for DevOps**

Allows flexible storage management.

### Structure:

```
Disk → PV → VG → LV → Filesystem
```

- **PV** → Physical Volume

- **VG** → Volume Group

- **LV** → Logical Volume


### Benefits:

- Resize storage without downtime

- Combine multiple disks

- Snapshots


Commands:

```bash
pvcreate
vgcreate
lvcreate
lvextend
```

👉 Interview line:

> “LVM abstracts physical storage and provides dynamic resizing and snapshots.”

---

# ⚡ 7. RAID (Redundant Array of Disks)

Used for:

- performance

- redundancy


### Types:

|RAID|Use Case|
|---|---|
|RAID 0|Fast, no redundancy|
|RAID 1|Mirroring|
|RAID 5|Parity|
|RAID 10|Best combo|

👉 DevOps context:

- Used in servers, cloud disks internally


---

# 📊 8. Disk Monitoring & Commands

### Must-know commands:

```bash
df -h  # disk usage
du -sh # folder size
lsblk  # block devices
mount  # mounted disks
blkid  # UUIDs
```

### Advanced:

```bash
iostat
iotop
```

👉 Interview tip:

> Always mention monitoring + troubleshooting

---

# 🚀 9. Performance Concepts

- SSD vs HDD vs NVMe

- IOPS (Input/Output ops per second)

- Throughput vs latency


👉 Example:

- DB → needs high IOPS

- Logs → sequential writes


---

# ☁️ 10. Cloud + DevOps Context (IMPORTANT)

### AWS Example:

- EBS → block storage

- S3 → object storage

- EFS → network filesystem


### Kubernetes:

- Persistent Volumes (PV)

- Persistent Volume Claims (PVC)


👉 Interview line:

> “Kubernetes abstracts storage using PV/PVC similar to how LVM abstracts disks.”

---

# 🔥 11. Real Interview Scenarios

### ❓ Disk full but `df` shows space?

- inode exhaustion

- deleted file still open


### ❓ How to extend disk?

- add disk → LVM → resize → `resize2fs`


### ❓ Logs filling disk?

- `/var/log` cleanup

- logrotate


---

# 🧠 12. Pro-Level Insights (This makes you stand out)

- `xfs` cannot shrink, only grow

- `ext4` supports both grow + shrink

- `tmpfs` uses RAM → super fast

- `noatime` mount option → improves performance

- UUID vs device names in `/etc/fstab`


---

# 🎯 How to Answer in Interview (Perfect Structure)

If asked:

👉 “Explain Linux filesystem”

Answer flow:

1. Definition

2. Storage stack (VFS)

3. Types (ext4, xfs…)

4. Mounting + FHS

5. Inodes

6. LVM

7. Real-world usage


---