---
title: Linux Linux Index
date: 2025-01-03
---


git all permissions to perticular dir

```
sudo chmod 777 .... .... .... ....
```



### 1. **To Check File Size**

Use the `ls -lh` command for a human-readable file size:

```bash
ls -lh
```

- `-l`: Long listing format
- `-h`: Human-readable sizes (e.g., KB, MB, GB)

Output Example:

```
-rw-r--r--  1 user user  4.0K Jan  3 12:00 example.txt
```

Here, `4.0K` is the size of the file.

---

### 2. **To Check Directory Size**

Use the `du` (disk usage) command:

```bash
du -sh [directory_name]
```

- `-s`: Summary of the total size
- `-h`: Human-readable format

Example:

```bash
du -sh /home/user
```

Output:

```
2.1G    /home/user
```

This shows the total size of the directory.

---

### 3. **To See Sizes of All Files and Subdirectories**

To list sizes of all files and subdirectories in a directory:

```bash
du -h [directory_name]
```

---

### 4. **Sort Files by Size**

Use `ls` with the `-S` flag to sort files by size:

```bash
ls -lSh
```

- `-S`: Sort by file size (largest first)
- `-h`: Human-readable

---

### 5. **Check Free Disk Space**

To see free and used disk space:

```bash
df -h
```

- `df`: Disk space usage
- `-h`: Human-readable format

Example Output:

```
Filesystem      Size  Used Avail Use% Mounted on
/dev/sda1       50G   20G   30G  40% /
```

---

Let me know if you need more help with CLI commands! 🚀




to assigin any command to shortcut 
```
alias k=kubectl #Directly inside terminal
```




# command to list all running processes, and filters the outpu

List processes

```
ps -ef | grep -i 
```




# grep command to show 10 lines below search

```shell
`openssl x509 -in /etc/kubernetes/pki/apiserver.crt -text -noout | grep -i -A 10 altern`
```