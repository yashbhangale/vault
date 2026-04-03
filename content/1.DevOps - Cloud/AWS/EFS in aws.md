---
title: EFS in aws
tags: [devops---cloud, aws]
---

![[Pasted image 20250918221959.png]]



![[Pasted image 20250918222022.png]]


![[Pasted image 20250918222051.png]]

---

---

## **Amazon EFS (Elastic File System)**

🔹 **Definition**:  
A **serverless, elastic, NFS-based file storage** service that can be mounted on multiple EC2 instances (Linux-based).

- Managed **shared file system** (POSIX-compliant).
- Automatically scales up/down with usage.

## **Key Features**

- **Fully managed** → No provisioning required.
- **Elastic** → Grows/shrinks automatically with data.
- **Shared access** → Multiple EC2s (thousands) can mount the same EFS.
- **Durability** → Data stored across multiple AZs (high availability).
- **Access via NFSv4 protocol**.
- **Lifecycle management** → Automatically move cold files to cheaper storage (EFS-IA).

## **Performance Modes**

1. **General Purpose** → Default, low latency (web servers, dev/test).
2. **Max I/O** → Higher throughput, higher latency (big data, analytics).

## **Storage Classes**

- **Standard (EFS Standard)** → Multi-AZ, highly durable.
- **Infrequent Access (EFS-IA)** → Lower-cost for rarely accessed files.

## **EFS vs EBS vs S3**

|Feature|**EFS**|**EBS**|**S3**|
|---|---|---|---|
|Type|Shared file system|Block storage|Object storage|
|Access|Multiple EC2s (multi-AZ)|One EC2 (single AZ)|Global, via HTTP API|
|Protocol|NFS|Attached volume|REST API|
|Scaling|Auto|Fixed size|Virtually unlimited|
|Durability|Across AZs|Single AZ (unless snapshot)|11 9’s across regions|

## **Use Cases**

- Web/app servers needing **shared storage**.
- Content management systems.
- Big data analytics.
- Container storage for **ECS/EKS**.
- Home directories for user apps.



![[Pasted image 20250918230656.png]]

