
# **COMPUTE SERVICES – DETAILED GIST**

## **Amazon EC2**

EC2 gives you virtual machines in the cloud. You choose the OS, CPU, RAM, storage, and networking.  
You manage updates, patches, scaling logic, and security groups.  
Used when you need full control over the server, custom software, or predictable compute workloads.

---

## **EC2 Auto Scaling**

This service monitors your EC2 fleet and automatically adds or removes instances based on metrics like CPU or request count.  
It helps you handle traffic spikes without manual intervention and saves money by scaling down when demand drops.  
Tightly integrates with load balancers.

---

## **Elastic Load Balancing (ALB, NLB)**

Load balancers distribute incoming traffic across multiple EC2 instances, containers, or IPs.  
ALB works at Layer 7 (HTTP/HTTPS) and supports path-based or host-based routing.  
NLB works at Layer 4 (TCP/UDP), is extremely fast, and is used for high-performance, low-latency workloads.  
This improves fault tolerance and availability.

---

## **AWS Lambda**

Lambda runs code in response to events without provisioning servers.  
You upload a function, choose runtime, and AWS handles execution, scaling, patching, and availability.  
It automatically scales to handle millions of requests.  
Best for APIs, automation, data processing, scheduled tasks, and microservices.

---

## **AWS Elastic Beanstalk**

A platform that deploys applications (Java, Node, Python, PHP, Go, Docker).  
You upload code, and Beanstalk creates EC2 instances, load balancers, autoscaling, and monitoring.  
You can override configs but generally it’s suited for developers who don’t want to manage infrastructure.

---

## **Amazon Lightsail**

Simplified compute service with predictable monthly pricing.  
Good for small websites, WordPress blogs, Minecraft servers, hobby apps, or simple databases.  
Comes with preconfigured OS + software stacks.

---

## **AWS Batch**

Manages batch computing jobs that need processing power.  
It automatically provisions compute resources and schedules jobs efficiently.  
Used for simulations, media rendering, big compute workloads.

---

## **AWS Outposts**

AWS rack installed in your on-prem data center.  
You can run AWS services (EC2, EBS, EKS) locally but with the same AWS APIs and tools.  
Used when you need low-latency local processing or data residency.

---

## **AWS Serverless Application Repository**

A catalog of prebuilt Lambda-based applications and components that you can deploy directly.  
Useful for quickly adding serverless features without building from scratch.

---

## **AWS Wavelength**

Brings AWS compute to telecom networks for ultra-low latency apps (gaming, AR/VR, IoT).  
Used when milliseconds matter.

---

## **AWS Local Zones**

AWS mini-regions placed closer to large cities.  
Used for workloads needing low latency but not full Outposts.

---

# **CONTAINERS – DETAILED GIST**

## **Amazon ECS (Elastic Container Service)**

AWS’s native container orchestration service.  
You define tasks (containers + config) and ECS schedules them on EC2 or Fargate.  
It integrates tightly with IAM, ALB/NLB, CloudWatch, and ECR.  
Good when you want a simpler alternative to Kubernetes while staying inside AWS.

---

## **Amazon EKS (Elastic Kubernetes Service)**

Managed Kubernetes control plane.  
AWS hosts and manages the Kubernetes API server, etcd, and control-plane components.  
You manage worker nodes or use Fargate for serverless pods.  
Ideal when you want portability (Kubernetes standard) or already know K8s.

---

## **AWS Fargate**

Serverless compute engine for containers.  
You run containers without launching EC2 instances.  
Works with ECS and EKS.  
AWS handles patching, provisioning, scaling, and security of underlying servers.

Use cases: microservices, lightweight APIs, event-driven container apps.

---

## **Amazon ECR (Elastic Container Registry)**

Private container image registry fully managed by AWS.  
Stores Docker images and integrates with ECS, EKS, CodeBuild, and CI/CD pipelines.  
Handles vulnerability scanning and encryption.

---

## **AWS App Mesh**

Service mesh for microservices running on ECS, EKS, EC2.  
Provides traffic control, observability, and consistent communication.  
Helps with retries, circuit breaking, service discovery, and monitoring.

Useful when you have many microservices and want centralized communication control.

---

## **AWS Cloud Map**

Service discovery tool for microservices.  
Services register themselves, and Cloud Map provides names and health checks.  
Useful for large distributed systems.

---

## **AWS Copilot**

Command-line tool to simplify deployment of containerized applications on ECS + Fargate.  
Not deeply asked in exams but good for practical DevOps use.

---

# **NETWORKING & CONTENT DELIVERY – DETAILED GIST**

## **Amazon VPC (Virtual Private Cloud)**

Your private isolated network inside AWS.  
You choose IP ranges, subnets (public/private), route tables, NACLs, and security groups.  
It’s the backbone for almost all AWS services.  
You control how your resources communicate with the internet, on-prem networks, and each other.

---

## **Subnets (Public + Private)**

- **Public subnet** connects to the internet through an Internet Gateway.
    
- **Private subnet** stays isolated unless you use NAT.  
    Used to create secure, multi-tier architectures (web → app → database layers).
    

---

## **Route Tables**

Tell subnets where to send traffic.  
Every subnet must be associated with a route table.  
Essential for controlling flow between VPC, subnets, NAT, IGW, TGW, etc.

---

## **Internet Gateway (IGW)**

Allows communication between your VPC and the public internet.  
Only subnets with IGW routes can be public.

---

## **NAT Gateway**

Let instances in **private subnets** access the internet (for updates, APIs) without exposing them publicly.  
Highly available and fully managed.

---

## **VPC Peering**

Direct connection between two VPCs.  
Good for small-scale, one-to-one communication.  
No transitive routing.

---

## **Transit Gateway**

A central hub that connects multiple VPCs, accounts, and on-prem data centers.  
Replaces complex VPC peering meshes.  
Used for large multi-VPC architectures.

---

## **AWS Direct Connect**

A dedicated physical fiber line from your data center to AWS.  
Lower latency, stable bandwidth, and more secure than VPN over the internet.  
Often used by enterprises.

---

## **VPN (Site-to-Site / Client VPN)**

Site-to-site: Connect your on-prem network to AWS over the public internet via encrypted tunnel.  
Client VPN: Users connect individually to AWS resources securely.

---

## **PrivateLink**

Lets you access AWS services, SaaS services, or your own services _privately_ without internet.  
Uses VPC endpoints (Interface Endpoints).  
Great for secure internal communication.

---

## **VPC Endpoints**

Private connections to AWS services without using the internet.  
Two types:

- **Interface Endpoint** (ENIs, PrivateLink)
    
- **Gateway Endpoint** (S3, DynamoDB)
    

Reduces latency and increases security.

---

## **AWS Global Accelerator**

Routes traffic over AWS’s high-speed global network instead of the public internet.  
Improves performance and gives static anycast IPs for your application.  
Helps with global users.

---

## **Amazon CloudFront**

AWS CDN that caches your content at edge locations worldwide.  
Speeds up websites, APIs, videos, and downloads.  
Works well with S3, ALB, Lambda@Edge, and Shield.

Used to reduce latency, improve security, and absorb DDoS attacks.

---

## **AWS WAF (Web Application Firewall)**

Applied on CloudFront, ALB, or API Gateway.  
Blocks common web exploits like SQL injection or XSS.  
Uses rules or managed rule sets.

---

## **AWS Shield**

DDoS protection service.

- **Standard** is free and protects against common attacks.
    
- **Advanced** gives enhanced protection and 24/7 response.
    

CloudFront + Route 53 get strongest protection.

---

## **Network Firewall**

Managed firewall inside your VPC.  
Controls outbound and inbound traffic with deep packet inspection.  
Good for enterprises needing strict security.

---

## **Route 53**

AWS’s DNS service.  
Used for:

- Domain registration
    
- DNS routing
    
- Health checks
    
- Failover  
    Supports routing policies like weighted, latency, failover, and geolocation.
    

High availability because it’s built across many edge locations.

---

## **Elastic Load Balancing (repeated for context)**

- **ALB**: HTTP/HTTPS, path routing, host routing, works with microservices
    
- **NLB**: Ultra-fast, millions of requests/sec, TCP/UDP
    
- **CLB**: Legacy, rarely used today
    

Load balancers help distribute traffic and improve fault tolerance.

---

## **AWS Cloud WAN**

Manages global wide area networks across multiple regions and branches.  
Enterprises use it to unify global connectivity in a single AWS-controlled network.

---

## **AWS App Mesh (Networking layer for microservices)**

Controls traffic routing between microservices.  
Adds features such as retries, circuit breaking, and detailed telemetry.  
Used with ECS/EKS/EC2 microservices.

---


# **STORAGE SERVICES – DETAILED GIST**

---

# **Amazon S3 (Simple Storage Service)**

Object storage for storing files, images, backups, logs, videos, datasets and application assets.  
It’s designed for **11 nines** durability and extreme scalability.  
Data is stored as objects in buckets, and you access them through URLs or APIs.  
You can configure lifecycle policies, encryption, versioning, cross-region replication, and storage classes.  
S3 integrates deeply with CloudFront, Lambda, Athena, Glue, and most AWS services.

**Why it’s important:** core storage service + heavily tested in exams.

---

# **S3 Storage Classes**

Different cost-performance tiers based on access frequency:

- Standard (frequent access)
- Standard-IA (infrequent)
- One Zone-IA (single AZ)
- Intelligent Tiering (auto moves data)
- Glacier Flexible Retrieval
- Glacier Deep Archive

Lifecycle rules automatically shift data to cheaper tiers.

---

# **S3 Glacier & Glacier Deep Archive**

Cold storage for long-term archiving with extremely low cost.  
Not meant for frequent access.  
Retrieval can take minutes to 12 hours depending on class.  
Used for compliance, backups, and historic data.

---

# **Amazon EBS (Elastic Block Store)**

Block storage volumes attached to EC2 instances.  
Behaves like a virtual hard drive.  
Supports different volume types for performance (gp3, io1, st1).  
Used for operating systems, databases, and low-latency workloads.  
Provides snapshots (backups) stored in S3.

---

# **EBS Snapshots**

Point-in-time backups of EBS volumes.  
Incremental and stored in S3.  
Used for disaster recovery, replication, and AMI creation.

---

# **Amazon EFS (Elastic File System)**

Fully managed network file system for Linux workloads.  
Automatically scales as you add/remove files.  
Shared across multiple EC2 instances, containers, or on-prem via Direct Connect.  
Ideal for web servers, CMS, shared storage, and multi-AZ workloads.

**Key property:** multi-AZ by default with high durability.

---

# **Amazon FSx Family**

Managed file systems optimized for specific workloads:

### **FSx for Windows File Server**

Fully managed Windows file system with SMB protocol.  
Used by Windows applications needing native Windows file features.

### **FSx for Lustre**

High-performance, low-latency file system for big data, HPC, and ML training.  
Often paired with S3.

### **FSx for NetApp ONTAP**

Enterprise-grade file system supporting NFS, SMB, iSCSI.  
Used for migration of enterprise workloads.

### **FSx for OpenZFS**

POSIX-compliant file system with high performance and snapshot features.

---

# **AWS Backup**

Centralized backup service for AWS resources.  
Supports EC2, EBS, RDS, DynamoDB, EFS, FSx, and on-prem backups.  
Automates backup plans, retention rules, vaults, and compliance controls.

Useful when you need audit-ready, managed backup at scale.

---

# **AWS Snow Family**

Physical devices for transferring huge amounts of data when network upload is slow.

### **Snowcone**

Small device for edge computing + transferring few TBs.

### **Snowball Edge**

Rugged device with compute + storage.  
Used for data migration (tens of TB) and edge processing.

### **Snowmobile**

A literal 45-foot shipping container for petabyte-scale transfer.

Used when you need to migrate entire data centers.

---

# **AWS Storage Gateway**

Hybrid storage service that connects on-prem applications to AWS storage.

Three types:

1. **File Gateway** – SMB/NFS shares → backed by S3
2. **Volume Gateway** – Block storage with EBS snapshots
3. **Tape Gateway** – Virtual tapes → backed by S3/Glacier

Used heavily in enterprise migrations.

---

# **Amazon DataSync**

Fast data transfer service for copying data between on-prem servers, S3, EFS, FSx.  
10x faster than regular copy tools.  
Great for large-scale migrations.

---

# **AWS Transfer Family**

Managed SFTP/FTP/FTPS server backed by S3 or EFS.  
Used when clients or companies require file transfer protocols.

---


# **DATABASE SERVICES – DETAILED GIST**

---

# **Amazon RDS (Relational Database Service)**

Fully managed SQL database service.  
Supports **MySQL, PostgreSQL, MariaDB, Oracle, SQL Server**.  
AWS handles patching, backups, snapshots, replicas, and failover.  
You choose instance size, storage, and AZ deployment.

**Why people use RDS:**  
You get the power of SQL without managing servers manually.  
Perfect for OLTP applications, websites, backend apps, and internal systems.

---

# **RDS Multi-AZ**

Creates a synchronous replica in another AZ.  
If the primary fails, RDS automatically fails over to the standby.  
Ensures high availability, not scaling.

---

# **RDS Read Replicas**

Asynchronous read-only copies of your primary database.  
Used to offload read traffic.  
Can exist across regions for global apps.

**Important:** They don’t provide automatic failover.

---

# **Amazon Aurora**

AWS's own high-performance relational database.  
Compatible with **MySQL and PostgreSQL**, but up to **5x faster**.  
Storage automatically scales up to 128 TB.  
Data is replicated across 6 copies in 3 availability zones.

Aurora comes in two forms:

- **Aurora Serverless** (auto-scaling DB, good for unpredictable workloads)
- **Aurora Provisioned** (more control + performance)

Ideal for enterprise apps, financial systems, SaaS platforms.

---

# **Amazon DynamoDB**

Fully managed NoSQL key-value and document database.  
Single-digit millisecond latency at any scale.  
Automatically scalable, serverless, and pay-per-request.  
Data is replicated across multiple AZs by default.

Used for:

- high-speed apps
- gaming
- e-commerce carts
- IoT
- real-time apps
**DynamoDB Streams** enable event-driven workflows.

---

# **DAX (DynamoDB Accelerator)**

In-memory cache for DynamoDB.  
Gives microsecond response times.  
Used when DynamoDB performance alone is not enough.

---

# **Amazon ElastiCache (Redis / Memcached)**

In-memory caching service.  
Improves performance by storing frequently accessed data in RAM.

Two engines:

- **Redis** – advanced features (pub/sub, streams, persistence)
- **Memcached** – simple, fast cache

Often used with:

- databases (reduces load)
- APIs
- high-traffic web apps
- session management

---

# **Amazon Redshift**

A fast, scalable **data warehouse** used for analytical workloads (OLAP).  
Optimized for large datasets and complex SQL queries across millions of rows.  
Integrates with S3 via Redshift Spectrum for big data querying.

Used for BI dashboards, reporting, analytics, and big data pipelines.

---

# **Amazon Neptune**

Graph database optimized for storing and querying highly connected data.

Supports two graph models:

- **Property Graph**
- **RDF/SPARQL**

Use cases:

- social networks
- fraud detection
- recommendation engines
- knowledge graphs

---

# **Amazon DocumentDB**

Managed **MongoDB-compatible** document store.  
Used when teams want MongoDB syntax but need AWS-managed reliability.

Works well for:

- JSON-heavy workloads
- content management
- catalogs
- user profiles

---

# **Amazon Keyspaces (Apache Cassandra)**

Fully managed, serverless Cassandra-compatible NoSQL database.  
Used for wide-column applications and massive scale workloads.

You get:

- no servers
- pay per request
- high availability by default

Often used by large-scale IoT, time-series, and large distributed apps.

---

# **Amazon Timestream**

Time-series database optimized for sensor, IoT, app monitoring, and telemetry data.  
Automatically manages data lifecycle (recent data stored in memory, old data in cost-efficient storage).

Use cases:

- IoT devices
- application metrics
- industrial telemetry

---

# **Amazon MemoryDB**

Redis-compatible primary database, not just cache.  
Stores data in memory for ultra-fast performance but adds durability with multi-AZ storage.

Used when Redis speed is needed with database reliability.

---

# **Amazon QLDB**

Quantum Ledger Database.  
Provides immutable, cryptographically verifiable transaction logs.  
Used when you need tamper-proof audit history.

Typical use cases:

- banking
- supply chain
- compliance systems
---

# **Database Migration Tools**

### **AWS DMS (Database Migration Service)**

Migrates databases to AWS with minimal downtime.  
Supports:

- homogeneous migrations (MySQL → MySQL)
- heterogeneous migrations (Oracle → PostgreSQL)

### **Schema Conversion Tool (SCT)**

Converts database schemas during migration.

---


# **SECURITY, IDENTITY & COMPLIANCE – DETAILED GIST**

---

# **AWS IAM (Identity and Access Management)**

This is the core service for authentication and authorization in AWS.  
You manage:

- Users
- Groups
- Roles
- Policies (JSON)

IAM decides **who can access what** and **what they can do**.  
It works on least-privilege and is global (not region-specific).

Key features:

- MFA
- Access keys
- IAM roles for EC2, Lambda, ECS tasks
- Permission boundaries
- Identity-based and resource-based policies

IAM is foundational for everything on AWS.

---

# **IAM Roles**

Temporary permissions given to AWS services or external identities.  
Used when you don’t want hardcoded credentials.  
Examples:

- EC2 role → gives an instance access to S3
- Lambda role → lets functions call DynamoDB
- SSO role → gives employees temporary console access

---

# **IAM Policies**

JSON documents defining what actions are allowed or denied.  
Attached to users, groups, or roles.

Two major types:

- AWS managed
- Customer managed (best for granular control)

---

# **AWS Cognito**

Handles **user sign-up, login, authentication**, and identity federation for your applications.

Components:

- **User Pools** – user database + signup/login + MFA
- **Identity Pools** – get temporary AWS credentials for users

Used when you need secure login without building your own authentication backend.

Common use cases:

- mobile apps
- SaaS products
- websites with login systems

---

# **AWS KMS (Key Management Service)**

Manages encryption keys (KMS keys).  
You can generate, rotate, store, and control keys.  
Integrated with almost all AWS services:

- S3
- EBS
- RDS
- DynamoDB
- Lambda
- SQS
- Secrets Manager

Supports symmetric and asymmetric keys.  
AWS never exposes the plaintext key.

Used for: encryption, compliance, secure-by-default architectures.

---

# **AWS Secrets Manager**

Stores sensitive data such as:

- database passwords
- API keys
- tokens

It can **automatically rotate secrets** (for RDS and others).  
You retrieve secrets securely via API or environment variables.  
More advanced and automated than Parameter Store.

---

# **SSM Parameter Store**

Stores configuration values and secrets (optionally encrypted with KMS).  
Cheaper than Secrets Manager but lacks automated rotation.  
Common for storing:

- environment variables
- app configs
- small secrets

Used heavily in CI/CD and system automation.

---

# **AWS WAF (Web Application Firewall)**

Protects against Layer 7 attacks:  
SQL injection, cross-site scripting, bot traffic, app layer threats.  
Applied at:

- CloudFront
- ALB
- API Gateway
- AppSync

Uses rule groups (managed or custom).  
Essential for securing APIs and web apps.

---

# **AWS Shield**

DDoS protection service.

Two tiers:

1. **Shield Standard** – automatic, free, protects CloudFront, Route 53, ALB
2. **Shield Advanced** – 24/7 DDoS response team, cost protection, deeper detection

Used heavily for large public-facing systems.

---

# **AWS CloudHSM**

Dedicated hardware security module cluster under your control.  
Gives full control over encryption keys.  
Used for highly regulated industries:

- banking
- government
- healthcare
- organizations with PKI requirements

More complex than KMS but offers stronger compliance.

---

# **Amazon GuardDuty**

Intelligent threat detection and continuous monitoring service.  
It analyzes logs from:

- CloudTrail
- VPC Flow Logs
- DNS Logs

Detects unusual behavior like:

- compromised IAM credentials
- malware behavior
- suspicious API calls
- unexpected network flows

Very important for security posture.

---

# **Amazon Inspector**

Automated vulnerability scanner for:

- EC2
- containers (ECR images)
- Lambda

Scans for:

- CVEs
- insecure configurations
- network reachability

Useful for DevSecOps workflows.

---

# **Amazon Macie**

Scans S3 buckets to find **sensitive data** such as:

- PII
- credit card numbers
- personal details

Uses machine learning to classify data.  
Helps with compliance audits.

---

# **Amazon Detective**

Helps investigate security issues by analyzing data from GuardDuty, CloudTrail, and VPC logs.  
Builds graphs that show relationships between events.

Used by security teams to understand the root cause of incidents.

---

# **AWS Security Hub**

Central dashboard that aggregates findings from:

- GuardDuty
- Inspector
- Macie
- IAM Access Analyzer
- Partner tools (CrowdStrike, Palo Alto)

Provides a single place for security compliance checks.  
Very useful for enterprise governance.

---

# **IAM Access Analyzer**

Identifies resources that are publicly accessible or shared with other accounts.  
Helps detect misconfigured policies.

---

# **AWS Certificate Manager (ACM)**

Manages SSL/TLS certificates for free.  
Used with:

- CloudFront
- ALB
- API Gateway

Handles automated renewal, making HTTPS setup easy.

---

# **Directory Services**

AWS managed Active Directory.  
Used when you need Windows authentication integration.

---
# **ANALYTICS SERVICES – DETAILED GIST**

---

# **Amazon Athena**

Serverless interactive query service that lets you query data directly from S3 using SQL.  
You don’t need servers, clusters, or databases.  
Just point Athena to your S3 bucket and run SQL queries.

Great for:

- log analysis
- quick data exploration
- ad-hoc queries
- analyzing CloudTrail logs

Powered by Presto under the hood.

---

# **AWS Glue**

Serverless ETL and data catalog service.

Glue provides:

1. **Crawlers** – scan S3 and auto-detect schema    
2. **Data Catalog** – central metadata store
3. **Glue ETL Jobs** – transform data (PySpark/Python)
4. **Glue Studio** – visual ETL tool

Essential for building data lakes.  
Frequently used with Athena, EMR, and Redshift.

---

# **Amazon EMR (Elastic MapReduce)**

Managed cluster platform for big data processing.  
Runs frameworks like:

- Spark
- Hadoop
- Hive
- Presto

You choose instance types, cluster size, and scaling options.

Used for:

- big data analytics
- data pipelines
- ML preprocessing
- log processing
- massive distributed workloads

Can integrate with S3 as storage (decoupled architecture).

---

# **Amazon Kinesis – Real-Time Data Platform**

Kinesis is for streaming data — logs, events, clicks, IoT signals.  
Four major services:

---

### **1. Kinesis Data Streams**

Real-time stream ingestion service.  
Producers send data → consumers process it in near real-time.

Used for:

- analytics dashboards
- fraud detection
- clickstream processing
- logs & metrics

---

### **2. Kinesis Data Firehose**

Fully managed delivery service for streaming data.  
Automatically sends incoming data to:

- S3
- Redshift
- OpenSearch
- Splunk

Firehose runs without servers and scales automatically.  
Good for log ingestion.

---

### **3. Kinesis Data Analytics**

Run SQL or Java/Flink applications on real-time Kinesis streams.  
Used for:

- real-time dashboards
- anomaly detection
- live metric transformations

---

### **4. Kinesis Video Streams**

Streams video from cameras and devices to AWS for playback, ML, or analytics.

---

# **Amazon Redshift**

AWS’s data warehouse for performing analytical queries on structured data at scale.  
Optimized for OLAP workloads, complex joins, aggregations, and large datasets.

Key features:

- Columnar storage
- Massively parallel processing (MPP)
- Redshift Spectrum (query S3 directly)

Used for BI dashboards, reporting, and analytics workloads.

Integrates with:

- QuickSight
- Glue
- S3
- Kinesis

---

# **Amazon OpenSearch Service**

Managed search and analytics engine based on Elasticsearch / OpenSearch.  
Used for:

- log analytics
- full-text search
- monitoring dashboards
- application observability

Often paired with Logstash or Kinesis Firehose.

---

# **AWS QuickSight**

BI dashboard service like Power BI or Tableau.  
Creates charts, dashboards, and reports from data in:

- S3
- Redshift
- Athena
- RDS
- DynamoDB

Can be embedded into apps.  
Pay-per-session pricing is cost-effective.

---

# **AWS Lake Formation**

Helps build and secure data lakes quickly on S3.  
Handles:

- permissions
- access control
- metadata
- ingestion
- governance

Simplifies the complex security model for data lakes.

---

# **AWS Data Exchange**

Marketplace for buying or sharing datasets securely.  
Used when you need third-party datasets (financial, geospatial, etc.)

---

# **AWS Glue DataBrew**

No-code data preparation tool.  
Helps clean, normalize, and transform data visually.

---

# **AWS Clean Rooms**

Enables secure data collaboration without sharing raw data.  
Useful for advertising and analytics where data privacy matters.

---

# **APPLICATION INTEGRATION – DETAILED GIST**

These services help applications communicate, pass messages, trigger workflows, integrate events, and connect SaaS applications.

Let’s break each one down properly.

---

# **Amazon SQS (Simple Queue Service)**

A fully managed message queue that decouples applications.  
Producers send messages → SQS stores them → consumers process them asynchronously.

Key points:

- Highly scalable and reliabl
- Messages are stored redundantly across AZs
- Consumers pull messages (not pushed)
- Prevents request overload on backend services
- Supports **Standard Queue** (high throughput) and **FIFO Queue** (ordering + exactly-once)

Use cases:

- Decoupling microservices
- Buffering workloads
- Job processing systems
- Offloading heavy tasks (image processing, ML pipelines)
SQS ensures that systems don’t break under load.

---

# **Amazon SNS (Simple Notification Service)**

A pub/sub messaging service.  
One message → multiple subscribers receive it.

Subscribers can be:

- Email
- SMS
- Mobile push
- HTTP endpoints
- Lambda
- SQS queues

Great for sending alerts or distributing messages to multiple systems.

Use cases:

- Fan-out patterns (SNS → multiple SQS queues)
- Alerts/notifications
- Triggering workflows in multiple systems

SNS is about **notifications**, SQS is about **queues**.

---

# **Amazon EventBridge**

Event bus for routing events between services and applications.  
You define rules based on incoming events → EventBridge forwards them to targets.

Targets include:

- Lambda
- Step Functions
- SQS
- SNS
- API Gateway
- EC2 / ECS tasks
- SaaS apps (Zendesk, Stripe, Auth0)

Use cases:

- Event-driven architectures
- Automated workflows
- Application monitoring
- SaaS integration

EventBridge is like the brain of event-driven cloud systems.

---

# **AWS Step Functions**

Workflow orchestration service.  
You break down a process into multiple steps and define how each step executes.

Supports:

- sequential steps
- parallel execution
- retries
- wait states
- branching logic

Each step can call:

- Lambda
- ECS tasks
- DynamoDB
- Glue
- SageMaker
- SNS / SQS
- API Gateway

Used for:

- long-running workflows
- microservice orchestration
- ML pipelines
- data processing pipelines

Step Functions helps you replace complex state machines in code with a visual workflow.

---

# **Amazon MQ**

Managed message broker for enterprise systems using:

- **ActiveMQ**
- **RabbitMQ**

Important for organizations that already depend on traditional messaging protocols:

- JMS
- AMQP
- MQTT
- STOMP

Why it's used:

- You don’t rewrite legacy systems
- AWS manages patching and scaling
- Smooth migration from on-prem to cloud

Unlike SQS/SNS, MQ supports **long-lived connections** and **complex message routing**.

---

# **Amazon AppFlow**

Fully managed data integration service.  
Moves data securely between SaaS apps and AWS.

Supports integrations with:

- Salesforce
- Slack
- Google Analytics
- Zendesk
- ServiceNow
- Marketo
- S3
- Redshift

Use cases:

- Syncing SaaS data into S3 for analytics
- Automating marketing data flows
- Sending updates from business apps to AWS

Best when you need no-code/low-code automation.

---

# **Amazon SWF (Simple Workflow Service)**

Legacy workflow service.  
Generally replaced by Step Functions, but still exists.

Used for:

- Complex, long-running human + machine workflows
- Systems needing manual approval steps
Not heavily tested now, but good to know.

---

# **AWS AppConfig** (part of SSM)

Used for application configuration management.  
Roll out config changes safely with:

- validation
- gradual rollout
- rollback mechanisms

Useful in microservices and large distributed systems.

---

# **Amazon EventBridge Scheduler**

Cron-like scheduled task runner with support for millions of schedules.  
Better and simpler than CloudWatch Events for scheduling jobs.

---


# **MANAGEMENT, MONITORING & GOVERNANCE – DETAILED GIST**

---

# **Amazon CloudWatch**

Monitoring and observability service for metrics, logs, alarms, dashboards, and events.

CloudWatch gives you:

- **Metrics** (CPU, memory, requests, custom metrics)
- **Logs** (application logs, Lambda logs, system logs)
- **Alarms** (trigger actions when metrics cross thresholds)
- **Dashboards** (visualize performance in one place)
- **CloudWatch Events / EventBridge** (automation based on system events)

Use cases:

- Monitor EC2, RDS, Lambda, ECS, API Gateway
- Set alarms for auto scaling
- View logs from distributed services
- Trigger actions when issues appear

CloudWatch is the central monitoring system in AWS.

---

# **AWS CloudTrail**

Records **every API call** made in your AWS account.  
Tracks:

- who called what
- from where
- what resources were affected
- whether the call succeeded

Helps with:

- security audits
- compliance
- troubleshooting
- governance

CloudTrail Logs are usually stored in S3 and analyzed using Athena.

**Every exam scenario involving “track changes” means CloudTrail.**

---

# **AWS Config**

Tracks configuration changes in your AWS resources over time.  
Shows:

- what changed
- when it changed
- who changed it
- whether it violates a compliance rule

It also supports **Config Rules**, which check for:

- open S3 buckets
- unencrypted EBS volumes
- unrestricted security groups
- non-compliant resources

Used for compliance, auditing, and governance.

CloudTrail = API history  
Config = resource configuration history

---

# **AWS Systems Manager (SSM)**

A massive suite of tools for automation and operations.

Important features:

- **SSM Agent** on EC2/on-prem
- **Run Command** – execute commands on servers without SSH
- **Session Manager** – SSH-less shell access to EC2 (very secure)
- **Parameter Store** – config and secrets
- **Patch Manager** – automate OS patching
- **Automation** – run playbooks
- **Inventory** – track OS/software data
- **State Manager** – enforce configuration policies

Used heavily by DevOps and sysadmins.

---

# **AWS Trusted Advisor**

Analyzes your AWS account and gives recommendations for:

- cost optimization
- security
- performance
- fault tolerance
- service limits

Trusted Advisor is like a cloud consultant built into AWS.

Free version gives basic checks.  
Premium (Business/Enterprise support) gives full checks.

---

# **AWS Organizations**

Manages multiple AWS accounts centrally.

Provides:

- multi-account structure
- consolidated billing
- service control policies (SCPs)
- account-level governance
- automatic provisioning of new accounts

Helps with enterprise setups, cost control, and strong security isolation.

Exam uses:

- blocking services for accounts → SCP
- central billing → Organizations
- multi-team isolation → separate accounts

---

# **AWS Control Tower**

A layer built on top of Organizations to automatically set up:

- secure multi-account environment
- logging
- guardrails
- account factory

Basically “quick start for multi-account architecture.”

Used by enterprises and organizations starting fresh on AWS.

---

# **AWS Budgets**

Set budgets and receive alerts when usage or spending exceeds thresholds.

Useful for:

- monthly cost control
- preventing bill shocks
- forecasting future cost

Works with Cost Explorer and emails/SNS alerts.

---

# **AWS Cost Explorer**

Visualizes and analyzes your AWS spending.  
Shows:

- cost trends
- service-wise breakdown
- daily/monthly usage
- cost anomalies

Helps optimize savings (especially EC2, S3, RDS).

---

# **AWS Health Dashboard**

Shows health of AWS services and how outages impact your resources.

Two types:

- **Service Health Dashboard** – global AWS status
- **Personal Health Dashboard** – impact on your specific resources

Useful for incident monitoring.

---

# **AWS License Manager**

Track and manage software licenses (Windows, SQL Server, Oracle).  
Helps avoid license overuse and violations.

---

# **AWS Resource Groups & Tag Editor**

Organizes and manages resources based on tags.  
You can search by resource type, tags, region, etc.

Useful for:

- cost allocation
- environment separation
- bulk resource updates

---

# **AWS Well-Architected Tool**

Provides automated reviews of your workloads based on the 6 WA pillars:

- operational excellence
- security
- reliability
- performance efficiency
- cost optimization
- sustainability

Used for optimizing cloud architecture.

---

Alright bro, here’s the full **MIGRATION + TRANSFER** section in the same medium-depth, clean, revision-friendly format.

---

# **MIGRATION & TRANSFER SERVICES – DETAILED GIST**

These services help you move **databases**, **servers**, **applications**, and **large datasets** from on-prem or other clouds into AWS.

---

# **AWS DMS (Database Migration Service)**

Fully managed service to migrate databases to AWS with **minimal downtime**.  
Supports both:

- **homogeneous migrations** (MySQL → MySQL, PostgreSQL → PostgreSQL)
- **heterogeneous migrations** (Oracle → PostgreSQL, SQL Server → Aurora)

Key features:

- Source DB stays live during migration
- Replicates ongoing changes (CDC → Change Data Capture)
- Works with on-prem, EC2, and RDS sources

Common use cases:

- migrating production databases
- switching DB engines
- offloading reporting DBs

For schema conversion → **use SCT (Schema Conversion Tool)** with DMS.

---

# **AWS Application Migration Service (AWS MGN)**

This is the primary service for **lift-and-shift** migrations.

It moves:

- full servers
- VMs
- on-prem workloads
- apps running on physical, VMware, Hyper-V, or cloud VMs

How it works:

- MGN agent replicates server disk blocks to AWS
- Creates an EC2 instance identical to your original server
- Supports test cutovers & production cutovers

Replaces the old Server Migration Service (SMS).

Best for:

- migrating entire infrastructures
- as-is migrations
- disaster recovery plan

---

# **AWS DataSync**

High-speed data transfer between:

- on-prem → AWS
- AWS → on-prem
- across AWS storage services (S3, EFS, FSx)

It’s **10x faster** than traditional copy tools (rsync, cp).

Supports transfers to/from:

- S3
- EFS
- FSx
- SMB/NFS on-prem storage
- Snow devices

Used for:

- large migrations
- incremental syncs
- backup jobs
- hybrid workloads

---

# **AWS Snow Family**

Physical devices for moving huge amounts of data when internet transfer is too slow or impossible.

### **1. Snowcone**

Small, rugged device (8 TB).  
Used for:

- small datasets
- edge computing
- remote sites or IoT deployments

### **2. Snowball Edge (Storage Optimized / Compute Optimized)**

Larger, rugged devices (80–210 TB).  
Support compute functions (EC2, Lambda) for edge processing.

Used for:

- petabyte-scale migration
- edge ML/analytics
- remote environments without stable internet

### **3. Snowmobile**

Massive 45-foot shipping container with 100 PB capacity.  
Used for **full datacenter migrations**.

---

# **AWS Transfer Family**

Managed transfer servers supporting traditional protocols:

- **SFTP**
- **FTP**
- **FTPS**

Backend storage is S3 or EFS.

Use cases:

- legacy enterprise transfers
- vendor/client file uploads
- automated integrations with S3-based systems

Completely replaces on-prem SFTP servers.

---

# **AWS Migration Hub**

Central dashboard to track all migration activities across:

- DMS
- MGN
- DataSync
- third-party tools

Offers:

- progress tracking
- performance insights
- migration metrics

Used in large-scale enterprise migrations to keep everything organized.

---

# **AWS SMS (Server Migration Service)** _(Legacy)_

Old service for migrating VMs to AWS.  
Now replaced by **Application Migration Service (MGN)**.  
Good to know the name for exam purposes but not used in real-world anymore.

---

# **AWS SCT (Schema Conversion Tool)**

Used when moving from **one DB engine to another**, like:

- Oracle → PostgreSQL
- SQL Server → Aurora
- MySQL → DynamoDB

It converts:

- tables
- indexes
- functions
- stored procedures
- views

Works together with DMS.

---

# **AWS CloudEndure** _(Legacy / DR)_

Before MGN, CloudEndure was used for disaster recovery and migration.  
Still appears in older materials but mostly replaced.

---

# **MACHINE LEARNING & AI SERVICES – DETAILED GIST**

These services provide ML training, inference, AI-powered APIs, and data intelligence.

---

# **Amazon SageMaker**

Full end-to-end machine learning platform.

It helps you:

- prepare data
- build models
- train models
- tune hyperparameters
- deploy models
- monitor models

You can use built-in algorithms or your own code (TensorFlow, PyTorch, Scikit-Learn).

Key components:

- **SageMaker Studio** – ML IDE
- **Training Jobs** – scalable distributed training
- **Inference Endpoints** – deploy models at scale
- **Pipeline** – CI/CD for ML
- **Notebook Instances** – Jupyter notebooks
- **Feature Store** – store/reuse ML features
- **Ground Truth** – labeling service

SageMaker is used when teams want managed ML without building infrastructure.

---

# **Amazon Rekognition**

AI service for analyzing **images and videos**.

Capabilities:

- object detection
- face detection
- face comparison
- label detection
- text extraction from images
- unsafe content detection

Used for:

- security cameras
- user identity verification
- image moderation
- retail analytics

Fully managed, no ML expertise needed.

---

# **Amazon Comprehend**

Natural Language Processing (NLP) service.

Understands text and can find:

- sentiment (positive/negative)
- key phrases
- entities (names, places, products)
- syntax
- topics

Use cases:

- customer feedback analysis
- social media analysis
- document understanding
- chatbot improvement

It’s serverless and powerful for text-based workloads.

---

# **Amazon Lex**

Service to build chatbots and voice bots.  
Uses the same technology as Alexa.

Features:

- natural language understanding
- automatic speech recognition
- context management
- connects with Lambda

Common uses:

- customer support bots
- booking assistants
- voice interfaces

Works with Contact Center (Amazon Connect).

---

# **Amazon Polly**

Text-to-speech service.  
Converts text into natural-sounding audio.

Useful for:

- IVR systems
- podcasts
- accessibility features
- voice-enabled apps

Supports many languages and tones.

---

# **Amazon Transcribe**

Speech-to-text service.  
Converts audio into accurate text.

Handles:

- multiple speakers
- noisy backgrounds
- custom vocabulary

Used for:

- call center transcription
- video subtitles
- meeting notes
- voice analytics

Often paired with Comprehend for sentiment analysis.

---

# **Amazon Translate**

Language translation service.

Features:

- fast
- neural machine translation
- supports many languages

Used when you need real-time translation for apps, chats, websites.

---

# **Amazon Textract**

Extracts text, tables, and form data from documents — PDFs, scans, images.

More advanced than OCR because it understands structure.

Use cases:

- invoice processing
- form automation
- ID verification
- document workflows

Often paired with Lambda or Step Functions for automated processing.

---

# **Amazon Forecast**

Time-series forecasting using ML.  
Same tech used by Amazon retail.

Used for:

- demand prediction
- inventory planning
- resource forecasting

You provide historical data → Forecast generates predictions.

---

# **Amazon Personalize**

Creates personalized recommendations (like Amazon.com).

Used for:

- product recommendations
- movie/music suggestions
- personalized rankings

Integrates easily with websites and apps.

---

# **Amazon Kendra**

Enterprise search engine powered by ML.

Can search across:

- SharePoint
- S3
- Google Drive
- databases
- internal documents

Understands natural language queries and returns relevant results.

Useful for companies with large document collections.

---

# **Amazon Fraud Detector**

AI service to detect fraud in:

- online payments
- account creation
- transactions
- identity verification

You upload historical data → it learns fraud patterns.

---

# **Amazon SageMaker Ground Truth**

Human-in-the-loop data labeling for ML datasets.  
Can use Mechanical Turk or private workforce.

Used for creating training data for vision/NLP models.

---

# **Amazon Bedrock**

Serverless platform for **foundation models and generative AI**.

Models from Amazon + third-party providers:

- Anthropic
- AI21
- Stability
- Meta LLaMA
- Amazon Titan models

Features:

- text generation
- chatbots
- embeddings
- summarization
- classification
- image generation

No infrastructure needed. Pay-per-use.

---

# **Lookout Services (ML-based anomaly detection)**

AWS provides ML-powered “Lookout for X” services:

### **Lookout for Metrics**

Automatically detects anomalies in time-series data.

### **Lookout for Vision**

Detects defects in manufacturing (product quality control).

### **Lookout for Equipment**

Predictive maintenance for industrial machines.

---

# **SERVERLESS + API SERVICES – DETAILED GIST**

These services help you build serverless apps, APIs, and real-time data flows.

---

# **AWS Lambda** _(already covered earlier but summarizing in API context)_

Runs code without servers.  
Triggers come from:

- API Gateway
- S3
- DynamoDB Streams
- EventBridge
- SNS / SQS
- CloudWatch Events

Autoscaling, pay-per-invocation, and fully managed runtime.  
Best for event-driven apps, automation, APIs, and microservices.

---

# **Amazon API Gateway**

A fully managed service to create, publish, secure, and monitor **REST APIs**, **HTTP APIs**, and **WebSocket APIs**.

Key features
- integrates with Lambda, EC2, ECS, DynamoDB
- request validation
- throttling & rate-limits
- API keys and usage plans
- caching to improve performance
- IAM, Cognito, and Lambda authorizers for authentication
- can serve as the front door for microservices or serverless apps

Use cases:

- serverless APIs with Lambda
- backend for web and mobile apps
- real-time chat apps (WebSocket)

---

# **AWS AppSync**

Managed GraphQL API service.  
Handles data fetching for mobile/web apps in a single request using GraphQL schema.

Data sources:

- DynamoDB
- Lambda
- RDS
- Elasticsearch/OpenSearch
- HTTP APIs

Supports real-time subscriptions.  
Common in modern frontend apps, SaaS dashboards, and real-time apps.

---

# **AWS Step Functions** _(already covered under integration but important for serverless)_

Orchestrates workflows with steps, retries, branching, and sequencing.  
You design flows visually, and Step Functions manage execution state.

Used for:

- serverless pipelines
- ML workflows
- ETL
- microservice workflows
---

# **Amazon EventBridge** _(brief recap in serverless context)_

Event bus that routes events between AWS services and SaaS apps.

Used when:

- building event-driven architectures
- decoupling microservices
- triggering Lambda functions based on events

---

# **Amazon SQS + SNS** _(serverless messaging recap)_

- **SNS** → broadcast notifications (push model)
- **SQS** → queue for processing (pull model)  
    Often used together in fan-out pattern.

---

# **AWS SAM (Serverless Application Model)**

Framework to build serverless apps using simple config files.  
Supports:

- Lambda
- API Gateway
- Step Functions
- DynamoDB

Lets you deploy full serverless stacks easily.

---

# **AWS CloudFront (Serverless Edge Logic)**

With **Lambda@Edge** and **CloudFront Functions**, you can run code at global edge locations.

Used for:

- header manipulation
- redirects
- authentication
- caching control

Good for high-performance global applications.

---

# **Amazon Cognito** _(serverless authentication)_

Fully managed signup, login, MFA, and identity federation for apps.  
Often used with API Gateway + Lambda.

---

Serverless section done bro.

Next up:

---

# **DEVELOPER TOOLS – DETAILED GIST**

These are CI/CD, code automation, version control, and DevOps tools from AWS.

---

# **AWS CodeCommit**

Private Git repositories hosted on AWS.  
Similar to GitHub or GitLab but fully managed inside AWS.  
Integrates with CodeBuild, CodePipeline, IAM.

Used for secure enterprise source control.

---

# **AWS CodeBuild**

Fully managed CI service to:

- compile code
- run tests
- build Docker images
- produce artifacts

Scales automatically and charges only for build minutes.

Often used with:

- CodePipeline
- ECR
- Lambda deployment

---

# **AWS CodeDeploy**

Automates application deployments.

Supports:

- EC2
- On-prem servers
- Lambda
- ECS

Deployment types:

- in-place
- blue/green

Used for safe, automated rollouts with rollback support.

---

# **AWS CodePipeline**

End-to-end CI/CD orchestration tool.  
Defines workflow:

- source → build → test → deploy

Integrates with:

- CodeCommit
- GitHub
- CodeBuild
- CodeDeploy
- Lambda
- CloudFormation
Used to automate full release pipelines.

---

# **AWS CodeArtifact**

Managed package repository for:

- npm
- Maven
- PyPI
- NuGet

Helps teams manage dependencies securely.

---

# **AWS Cloud9**

Cloud-based IDE that runs in the browser.  
Has terminal, debugger, and all AWS CLI tools built-in.  
Useful for:

- students
- remote teams
- serverless development

---

# **AWS X-Ray**

Distributed tracing system to analyze how requests flow through applications.

Tracks:

- latency
- bottlenecks
- downstream calls
- errors in microservices

Used heavily in Lambda, API Gateway, ECS, EKS apps.

---

# **AWS CodeStar (less used now)**

Unified interface for creating CI/CD project templates.  
Integrates with CodeCommit, CodeBuild, CodeDeploy, CodePipeline.

Not widely used anymore but still exists.

---
