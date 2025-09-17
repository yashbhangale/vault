## **AWS EC2 (Elastic Compute Cloud)**

🔹 **Definition**:  
EC2 is a virtual server in the AWS cloud. It provides resizable compute capacity to run applications.

---

### **Key Concepts**

- **AMI (Amazon Machine Image)** → Template with OS + software, used to launch instances.
- **Instance Types** → Different combinations of CPU, memory, storage, networking. (e.g., t2.micro, m5.large)
- **EBS (Elastic Block Store)** → Persistent storage attached to EC2.
- **Instance Store** → Temporary storage, data lost on stop/terminate.
- **Security Groups** → Virtual firewall (instance-level).
- **Key Pairs** → SSH login (Linux) / RDP (Windows).
- **Elastic IP** → Static public IP for an instance.
- **Placement Groups** → How instances are placed on hardware (Clustered, Spread, Partition).

---

### **Lifecycle**

1. **Launch** → Choose AMI, instance type, VPC/subnet, storage, SG.
2. **Running** → Instance active, can connect via SSH/RDP.
3. **Stop/Start** → Preserves EBS but changes public IP (unless Elastic IP used).
4. **Terminate** → Instance + EBS (if not kept) deleted.

---

### **Pricing Models**

- **On-Demand** → Pay per second/hour, no commitment.
- **Reserved** → 1-3 year contract, cheaper (~75% less).
- **Spot** → Bid on unused capacity, very cheap, can be interrupted.
- **Dedicated Hosts/Instances** → Physical server dedicated to you.
---

### **Scaling**

- **Auto Scaling Group (ASG)** → Automatically add/remove EC2s based on demand.
- **Elastic Load Balancer (ELB)** → Distributes traffic across multiple EC2s.

---

### **Use Cases**

- Running web servers, backend apps.
- Hosting databases (non-managed).
- High-performance computing.
- Batch jobs.

---


![[Pasted image 20250916194038.png]]


![[Pasted image 20250916220229.png]]

---

## **AWS Security Group (SG)**

🔹 **Definition**:  
A **virtual firewall** at the **instance level** (works on EC2, RDS, Lambda in VPC, etc.). It controls **inbound (ingress)** and **outbound (egress)** traffic.

---

### **Key Properties**

- **Stateful** → If inbound is allowed, response is automatically allowed (no need to define outbound).
- **Instance-level** → Applied to EC2/network interfaces, not subnets.
- **Default SG** → Created with every VPC; allows all outbound but no inbound.
- **Rules** → Allow only (❌ no deny option). Deny is handled by **NACLs**.

---

### **Rules**

- **Inbound rules** → Define what traffic is allowed _into_ instance. (e.g., allow SSH from `0.0.0.0/0`)
- **Outbound rules** → Define what traffic can leave. (Default: allow all)
- **Protocol/Port/IP** → Rules specify protocol (TCP/UDP/ICMP), port (22, 80, 443), and source/destination (IP, CIDR, SG).

---

### **Limits**

- Up to **5 SGs** per ENI (Elastic Network Interface).
- Up to **60 inbound + 60 outbound rules** per SG (soft limit, can be increased).

---

### **Difference vs NACL**

|**Security Group**|**Network ACL**|
|---|---|
|Instance-level|Subnet-level|
|Stateful|Stateless|
|Only **allow** rules|Allow + Deny|
|Applied to ENI/EC2|Applied to entire subnet|


![[Pasted image 20250916220838.png]]



classic ports

ssh port 22
ftp 21 
sftp 22
http 80
https 443
RDP 3389

![[Pasted image 20250916220944.png]]
 





![[Pasted image 20250916222427.png]]

---
## **SSH (Secure Shell)**

🔹 **Definition**:  
A secure protocol to **remotely access and manage servers** over an encrypted connection.
- Default port: **22**
- Replaces insecure protocols like Telnet.

---

### **How SSH Works**

1. **Client → Server** connection.
2. Authentication via:
    - **Username + Password**, OR
    - **Key Pair** (private key on client, public key on server).
3. Encrypted communication channel established.

---

## **1. SSH in Linux/Mac**

🔹 Native SSH client is built-in.
### **Steps**:

1. Open terminal.
2. Run:

    ```bash
   ssh -i /path/to/private-key.pem username@server-ip
  ```
    - `-i` → Identity file (private key).
    - `username` → Commonly `ec2-user`, `ubuntu`, or `root` (depends on AMI).
    - Example:
```bash
        ssh -i mykey.pem ubuntu@54.201.123.45
 ```

---

## **2. SSH in Windows**

🔹 Two ways:
### **A. Using PowerShell/Command Prompt (Windows 10+)**

1. Place `.pem` key in safe folder.
2. Run:
    ```powershell
    ssh -i C:\path\to\mykey.pem username@server-ip
    ```
    
    Example:
    ```powershell
    ssh -i C:\Users\Yash\Downloads\mykey.pem ec2-user@3.120.45.67
    ```
    

---

### **B. Using PuTTY (if older Windows)**

PuTTY doesn’t support `.pem` directly → need `.ppk`.

1. Use **PuTTYgen** to convert `.pem → .ppk`.
2. Open PuTTY → Enter `username@server-ip`.
3. In **Connection > SSH > Auth**, browse and select `.ppk`.
4. Open → Login.

---

## **Common Issues**

- **Permission denied** → Wrong username or key.
- **Key file unprotected** → Fix with:

 ```bash
   chmod 400 mykey.pem
  ```
- **Port blocked** → Ensure **Security Group allows port 22 inbound**.

---


## **Using AWS Console (EC2 Instance Connect)**

- Works only for **Amazon Linux 2** & **Ubuntu**.
- No need for SSH key.
- Console → EC2 → Select instance → **Connect → EC2 Instance Connect → Connect**.
- A browser-based SSH session opens.


## use IAM rules for ec2 instances

---

![[Pasted image 20250916231501.png]]


![[Pasted image 20250916232004.png]]


![[Pasted image 20250916232018.png]]