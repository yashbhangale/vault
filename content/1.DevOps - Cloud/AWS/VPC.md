---
title: VPC
tags: [devops---cloud, aws]
---

## 🧠 1. What is a VPC?

A **VPC (Virtual Private Cloud)** is your **own private network inside AWS**.  
You control everything — IP ranges, subnets, routing, and security.

Think of it like your **own house** inside AWS.  
Each room (subnet) has a specific purpose — one for guests (public), one for personal use (private).

---

## 🧩 2. Key Components of VPC

### 1. **CIDR Block**

- Defines your VPC’s IP address range.    
- Example: `10.0.0.0/16` → gives you 65,536 IPs.
- Smaller subnets (like `/24`) have 256 IPs.
- You can’t overlap CIDR blocks if you want VPC peering later.
---

### 2. **Subnets**

- Subnets divide your VPC into smaller networks.
- Each subnet lives in **one Availability Zone** only.
- **Public Subnet:** has internet access (for web servers).
- **Private Subnet:** internal use only (for DBs, backend services).

---

### 3. **Internet Gateway (IGW)**

- A gateway that lets instances in public subnets access the internet.    
- Without it, even public instances can’t reach outside.

**Example flow:**  
Public EC2 → Route Table → IGW → Internet

---

### 4. **NAT Gateway / NAT Instance**

- Used by private subnets to reach the internet **without being exposed**.    
- Example: private EC2 downloading OS updates.
- NAT Gateway sits in the **public subnet** and routes traffic for private ones.

---

### 5. **Route Tables**

- Define **where network traffic should go**.
- Each subnet must be associated with one route table.    
- Example:
    - Public subnet → route to IGW (`0.0.0.0/0 → IGW`)
    - Private subnet → route to NAT (`0.0.0.0/0 → NAT GW`)

---

### 6. **Security Groups (SGs)**

- Instance-level firewalls.    
- Control **inbound and outbound** traffic.
- **Stateful:** if inbound is allowed, return traffic is automatically allowed.    

---

### 7. **Network ACLs (NACLs)**

- Subnet-level firewalls.    
- **Stateless:** need to define inbound and outbound separately.
    
- Add an extra layer of protection to your network.
    

---

### 8. **VPC Peering**

- Connects two VPCs privately (no internet in between).
    
- Works only for non-overlapping CIDR blocks.
    
- **Not transitive:** A↔B and B↔C doesn’t mean A↔C.
    

---

### 9. **VPC Endpoints**

- Connect AWS services (like S3, DynamoDB) privately without using the internet.
    
- Two types:
    
    - **Gateway Endpoint:** for S3, DynamoDB.
        
    - **Interface Endpoint:** for most other services.
        

---

### 10. **VPC Flow Logs**

- Capture network traffic logs in your VPC.
    
- Useful for debugging and auditing.
    
- Logs go to CloudWatch or S3.
    
- Note: they don’t log DNS or Windows license traffic.
    

---

## 🧰 3. Default vs Custom VPC

|Feature|Default VPC|Custom VPC|
|---|---|---|
|Automatically created|✅ Yes|❌ No|
|Internet access ready|✅ Yes|❌ Manual setup|
|Subnets|1 per AZ|You decide|
|Route tables, IGW|Preconfigured|You configure|
|Best for|Testing or learning|Production|

> Default VPC is plug-and-play, but custom VPC gives full control and security.

---

## 🧠 4. Analogy for Easy Understanding

|Concept|Analogy|
|---|---|
|VPC|Your house|
|Subnet|Each room in the house|
|Route Table|Directions board for where to go|
|Internet Gateway|Main door (to the outside world)|
|NAT Gateway|Secret door — you can go out, but no one can come in|
|Security Group|Door lock on a specific room|
|NACL|Boundary wall around the house|

---

## 📘 5. AWS Associate Exam Tips

1. **Subnets = 1 AZ only** (they can’t span across AZs).
    
2. **NAT Gateway must be in public subnet.**
    
3. **Security Groups = Stateful**, **NACLs = Stateless.**
    
4. **Default NACL** allows everything in/out.
    
5. **VPC Peering isn’t transitive.**
    
6. **VPC CIDR blocks can’t overlap** for peering.
    
7. **Flow logs** don’t record DNS or Windows license traffic.
    
8. **IGW is required** for public internet access.
    

---

## ⚙️ 6. Example Architecture

```
VPC: 10.0.0.0/16
│
├── Public Subnet (10.0.1.0/24)
│     ├── EC2 Instance (Web Server)
│     └── Route → IGW
│
├── Private Subnet (10.0.2.0/24)
│     ├── EC2 Instance (App Server)
│     └── Route → NAT Gateway → IGW
│
└── Security:
      ├── SG: Allow HTTP (80), SSH (22)
      └── NACL: Allow inbound 80, outbound 443
```

---

## 💡 Bonus (for real-world + exam)

- Always have **at least two subnets** in different AZs for **high availability**.
    
- For production, place DBs in **private subnets**.
    
- Use **VPC Endpoints** instead of public S3 access for better security.
    
- Use **Flow Logs + CloudWatch** to monitor traffic patterns.
    

---

If you want, I can make a **clean Excalidraw diagram** of this architecture (public/private subnet, NAT, IGW, etc.)  
Would you like me to make that visual next?

Also, I can prepare a **set of 15 VPC-based AWS exam questions** with explanations — perfect for practice before your certification. Want that too?