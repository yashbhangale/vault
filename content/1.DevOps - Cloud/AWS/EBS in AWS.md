---
title: EBS in AWS
tags: [devops---cloud, aws]
---

## **Amazon EBS (Elastic Block Store)**

🔹 **Definition**:  
EBS is a **block-level storage** service that provides persistent storage volumes for **EC2 instances**.
- Works like a **virtual hard disk**.
- Survives instance stop/start (unlike instance store).

### **Key Features**

- **Persistent** → Data is retained even if instance is stopped/terminated (if `DeleteOnTermination = false`).
- **Block storage** → Low-latency, random read/write access.
- **Replicated in AZ** → Data automatically replicated within the same AZ for durability.
- **Attach/Detach** → Volumes can be attached/detached from EC2s in the same AZ.
- **Snapshots** → Point-in-time backups stored in S3 (can be copied to other regions).
- **Encryption** → At-rest & in-transit with AWS KMS.
### **Types of EBS Volumes**

|**Type**|**Use Case**|
|---|---|
|**gp3 (General Purpose SSD)**|Default; balance of price/performance.|
|**gp2 (Older GP SSD)**|Still used; performance scales with size.|
|**io2/io2 Block Express (Provisioned IOPS SSD)**|High-performance workloads (databases, critical apps).|
|**st1 (Throughput Optimized HDD)**|Big data, data warehouses, log processing.|
|**sc1 (Cold HDD)**|Lowest cost, infrequent access, archival.|

### **Performance**

- Measured in **IOPS (Input/Output Operations per Second)** & **Throughput (MB/s)**.
- gp3 → 3,000 IOPS baseline (independent of size).
- io2 → Up to 256,000 IOPS (enterprise-grade).

### **EBS vs Instance Store**

|**EBS**|**Instance Store**|
|---|---|
|Persistent|Ephemeral (data lost on stop/terminate)|
|Can take snapshots|❌ No snapshots|
|Slower than instance store|Very fast (direct hardware)|
|Extra cost|Included with instance|

---

## EBS SNAPSHOTS

![[Pasted image 20250918214602.png]]


![[Pasted image 20250918214616.png]]



![[Pasted image 20250918221222.png]]






