
![[Pasted image 20250918215534.png]]

## **Amazon Machine Image (AMI)**

🔹 **Definition**:  
An **AMI is a template** used to launch an EC2 instance.  
It includes:

1. **OS** (Linux/Windows)
2. **Application software** (e.g., web server, DB)
3. **Launch permissions** (who can use it)
4. **Block device mapping** (storage volumes attached)

---

## **Types of AMIs**

1. **AWS-provided** → Standard OS images (Amazon Linux, Ubuntu, Windows).
2. **Marketplace AMIs** → Pre-configured images from vendors (e.g., WordPress, Red Hat).
3. **Custom AMIs** → Created by users (e.g., with your apps pre-installed).
4. **Community AMIs** → Shared by others (use with caution).

---

## **AMI Lifecycle**

1. Launch instance → Configure (install apps, packages).
2. Create AMI from the instance → Stored in Amazon S3 (managed by AWS).
3. Use AMI to launch **identical instances** anytime.

---

## **Benefits**

- **Consistency** → Launch multiple identical servers.
- **Faster deployments** → No need to reconfigure every time.
- **Backup** → Save system state & reuse later.
- **Sharing** → Share AMIs across accounts or regions.

---

## **AMI vs Snapshot**

|**AMI**|**Snapshot**|
|---|---|
|Full template (OS + apps + configs + block device mapping)|Backup of one EBS volume|
|Used to launch new EC2 instances|Used to create AMIs or restore EBS volumes|
|Can contain multiple snapshots (root + data volumes)|Single volume only|

## **Use Cases**

- Custom web servers (e.g., pre-installed Apache, PHP)
- Golden images for DevOps (standard baseline AMI).
- Disaster recovery (store AMI as backup).




![[Pasted image 20250918215915.png]]


![[Pasted image 20250918215952.png]]

