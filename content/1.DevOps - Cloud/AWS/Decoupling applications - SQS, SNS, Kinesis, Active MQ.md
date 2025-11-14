SQS queues

### **1. Introduction**

- **Amazon SQS (Simple Queue Service)** is a **fully managed message queuing service** by AWS.    
- It helps **decouple microservices, distributed systems, and serverless applications** by allowing asynchronous communication.
- You can think of it as a **temporary storage for messages** that travel between different components of your application.
---
### **2. Key Concepts**

- **Producer (Sender):** Sends messages to the queue.
- **Consumer (Receiver):** Retrieves and processes messages from the queue.
- **Queue:** The buffer that temporarily stores messages until they’re processed.
- **Message:** The actual data being transmitted (up to 256 KB per message)
---

### **3. Types of Queues**

1. **Standard Queue:**
    - Offers **high throughput** (nearly unlimited transactions per second).
    - **At-least-once delivery** (a message might be delivered more than once).
    - **Best-effort ordering** (message order isn’t guaranteed).

2. **FIFO Queue (First-In-First-Out):**    
    - Ensures **exactly-once processing** and **message order preservation**.
    - Throughput: up to **300 messages per second** (or higher with batching).
    - Used when **order and duplication control** are critical.
---

### **4. Message Lifecycle**

1. A producer **sends** a message to the queue.
2. The message is **stored** in SQS until a consumer retrieves it.
3. The consumer **polls** the queue (short or long polling) to get messages.
4. Once received, the message becomes **invisible** for a short period (Visibility Timeout).
5. After processing, the consumer **deletes** the message.
6. If not deleted within visibility timeout, the message **reappears** for reprocessing.
---

### **5. Visibility Timeout**

- Time during which a retrieved message remains **invisible** to other consumers.
- Prevents multiple consumers from processing the same message simultaneously.
- Default: **30 seconds** (max 12 hours).
---

### **6. Dead Letter Queue (DLQ)**

- A **separate queue** to store messages that couldn’t be processed successfully after multiple attempts.
- Helps identify and troubleshoot problematic messages.
---

### **7. Message Retention**

- Messages can be stored from **1 minute to 14 days** (default: 4 days).
- Useful for handling temporary service failures.
---

### **8. Polling Mechanisms**

1. **Short Polling:** Immediately returns even if no messages are available.
2. **Long Polling:** Waits for messages to arrive before responding (reduces cost and empty responses).
---

### **9. Security**

- Integrates with **AWS IAM** for access control.
- Supports **encryption at rest (KMS)** and **in transit (SSL/TLS)**.
- Fine-grained permission policies for send, receive, or delete actions.
---

### **10. Cost and Pricing**

- Pay for **number of requests** and **payload size** (no upfront costs).
- Very **cost-efficient** for large-scale distributed systems.
---

### **11. Integration**

- Works seamlessly with:
    - **AWS Lambda** (trigger functions on message arrival)
    - **SNS (Simple Notification Service)** for pub/sub model
    - **EC2, ECS, Step Functions, CloudWatch, etc.**
---

### **12. Use Cases**

- Decoupling microservices    
- Asynchronous job processing
- Order processing systems
- Task scheduling and background job queues
- Buffering requests during high traffic
---

### **13. Real-world Example**

Suppose you run an e-commerce site:
- When an order is placed, the **order service** sends a message to an **SQS queue**.
- A **payment service** picks up messages one by one and processes payments asynchronously.
- If something fails, messages go to a **DLQ** for later review.
---


# SNS


### **1. Introduction**

- **Amazon SNS (Simple Notification Service)** is a **fully managed pub/sub messaging service** by AWS.    
- It allows **decoupled communication** between different application components.
- It can **send messages to multiple subscribers** simultaneously — like broadcast notifications    
---

### **2. Core Concept: Pub/Sub Model**

- **Publisher (Producer):** Sends a message to a **topic**.
- **Subscriber (Consumer):** Receives messages from that topic.
- **Topic:** A logical access point where publishers send messages and subscribers listen.
➡️ **One-to-many communication model** — one publisher can send messages to many subscribers at once.
---

### **3. Message Flow**

1. **Publisher** publishes a message to a **topic**.    
2. **SNS Topic** distributes the message to all **subscribers** of that topic.
3. **Subscribers** receive the message via their configured endpoint (e.g., email, Lambda, SQS, HTTP)    
---

### **4. Supported Subscribers (Endpoints)**

- **SQS Queue** → for reliable message processing.
- **AWS Lambda** → trigger serverless functions automatically.
- **Email / SMS / Mobile Push Notifications.**
- **HTTP/HTTPS endpoints** → for webhooks and external APIs.
- **Kinesis Data Firehose** → for streaming data pipelines.
---

### **5. Key Features**

- **Pub/Sub Messaging:** Decouple microservices and event-driven apps.
- **Fan-out Pattern:** A single message sent to SNS can trigger multiple actions simultaneously.
- **Durable Delivery:** Retries until a subscriber successfully receives the message.
- **Encryption:** Supports KMS encryption for data at rest.
- **Access Control:** Uses IAM policies to restrict who can publish or subscribe.
---

### **6. Message Delivery**

- **Push-based system** → SNS _pushes_ messages to subscribers (unlike SQS which is _pull-based_)
- For failed deliveries, SNS can retry automatically or move messages to a **Dead Letter Queue (DLQ)**.
---

### **7. Message Filtering**

- Subscribers can use **message attributes** and define **filter policies**.
- Only messages matching the filter are delivered.  
    Example:

  ```json
    { "eventType": "order_placed" }
    ```

    → Subscriber only receives “order_placed” messages.    

---

### **8. Security**

- **IAM Policies:** Control who can publish/subscribe.    
- **Encryption:** KMS for encryption at rest.
- **HTTPS / TLS:** For secure message delivery in transit.
- **Access Policies:** Restrict topics to specific accounts or services
---

### **9. Integrations**

- SNS works seamlessly with:
    - **SQS** (for reliable processing)
    - **Lambda** (for event-driven workflows)
    - **CloudWatch** (for alerts
    - **Step Functions** (for orchestration
    - **Mobile Push Notifications** (for users)
---

### **10. Cost**

- Pay per **request (publish)** and **delivery attempts**.
- No upfront cost — pay-as-you-go model.
---

### **11. Use Cases**

- Application & system alerts (via email/SMS)    
- Event-driven workflows
- Fan-out data to multiple systems
- Decoupled microservice communication
- Mobile push notifications
---
### **12. Real-world Example**

Imagine an **e-commerce app**:

- When a new order is placed → an **SNS topic (OrderTopic)** is triggered.    
- Subscribers:
    - **Lambda** → send confirmation email
    - **SQS** → log for analytics
    - **SMS endpoint** → notify delivery team
➡️ One event → multiple parallel actions.

---

### **13. SNS vs SQS (Quick Comparison)**

| Feature           | **SNS**                           | **SQS**                 |
| ----------------- | --------------------------------- | ----------------------- |
| Type              | Pub/Sub (Push)                    | Queue (Pull)            |
| Communication     | One-to-many                       | One-to-one              |
| Delivery          | Push messages                     | Consumers poll messages |
| Order Guarantee   | No                                | FIFO queue (optional)   |
| Message Retention | No (just delivers)                | 1 min – 14 days         |
| Integration       | Triggers Lambda, HTTP, SQS, Email | Consumed by workers     |

---

# Kinesis
### 1. Introduction

- **Amazon Kinesis Data Streams (KDS)** is a **real-time data streaming service** by AWS.
- It helps you collect, process, and analyze continuous data streams such as logs, metrics, events, or IoT data.
- It’s used when you need immediate insights rather than batch processing.

---

### 2. Core Concept

Kinesis Data Streams works like a real-time pipeline.  
Producers continuously send data to a stream, which holds it temporarily. Multiple consumers can read and process the same data independently.

---

### 3. Key Components

| Component         | Description                                                                  |
| ----------------- | ---------------------------------------------------------------------------- |
| **Producer**      | Sends (writes) data records to the stream, e.g., apps, servers, IoT devices. |
| **Stream**        | A channel that transports and stores data temporarily.                       |
| **Shard**         | A capacity unit that defines how much data can be ingested or read.          |
| **Data Record**   | A single data entry (up to 1 MB).                                            |
| **Partition Key** | Determines which shard the record goes to.                                   |
| **Consumer**      | Reads and processes data from the stream.                                    |

---

### 4. Data Flow

1. Producers send data to the **Kinesis Stream**.    
2. The stream distributes data across multiple shards.
3. Consumers read data from shards in real time.
4. Data automatically expires after the retention period (default 24 hours).

---

### 5. Shards

- Each stream is made up of one or more shards.    
- Each shard provides:
    - Write: Up to **1 MB/sec** or **1,000 records/sec**.
    - Read: Up to **2 MB/sec**.
- You can scale by adding or merging shards as needed.    

---

### 6. Retention Period

- Default: **24 hours**.
- Can be extended up to **7 days** or **365 days** with extended retention.
- After the retention period, data is automatically deleted.

---

### 7. Consumers

**1. Shared (Classic) Consumer:**

- Uses the `GetRecords()` API.    
- Limited to 2 MB/sec read per shard.

**2. Enhanced Fan-Out Consumer:**

- Each consumer gets its own dedicated 2 MB/sec throughput.
- Very low latency (less than 70 ms).
- Useful for multiple consumers reading the same stream simultaneously.    
---

### 8. Data Processing

You can process Kinesis data with:
- **AWS Lambda:** Event-driven processing.
- **Kinesis Data Analytics:** Run SQL-like queries on the stream.
- **Kinesis Firehose:** Deliver data automatically to S3, Redshift, or OpenSearch.
- **Custom Consumers:** Apps running on EC2, ECS, or containers.
---

### 9. Security

- **IAM policies** control access to streams.
- **KMS encryption** secures data at rest.
- **SSL/TLS** protects data in transit.
- **VPC endpoints** allow private access within your network.
---

### 10. Monitoring and Scaling

- Use **CloudWatch metrics** to monitor read/write throughput, shard usage, and iterator age.    
- Use **Application Auto Scaling** to adjust the number of shards automatically based on workload.
---

### 11. Common Use Cases

- Real-time analytics on application logs or stock trades.    
- IoT data streaming from connected devices.
- Monitoring and observability pipelines.
- Clickstream analysis for user behavior.
- Event-driven workflows triggering AWS Lambda.

---

### 12. Pricing

You pay for:
- The number of **shards** provisioned (per hour).    
- **PUT payload units** (data written).
- **Data retention** duration.
- **Enhanced Fan-Out** consumers (if enabled).
---

### 13. Real-world Example

A food delivery app uses Kinesis Data Streams to track live order data:

1. Each app instance sends order updates to the stream.
2. The stream stores data across multiple shards.
3. Lambda functions consume the data to update real-time dashboards.
4. Firehose stores raw data into S3 for long-term analytics.

---

### 14. Kinesis Data Streams vs Firehose

|Feature|**Kinesis Data Streams**|**Kinesis Firehose**|
|---|---|---|
|Management|Developer-managed|Fully managed|
|Latency|Milliseconds|1–5 minutes|
|Data Processing|Real-time (custom apps/Lambda)|Automatic delivery to storage|
|Control|Fine-grained|Minimal|
|Use Case|Complex, real-time apps|Simple data ingestion to S3, Redshift, etc.|

---

### 15. Summary

- **Kinesis Data Streams** enables real-time data ingestion and processing.
- Highly scalable via shards
- Integrates with Lambda, Firehose, and Kinesis Analytics.
- Best suited for live dashboards, event-driven systems, and continuous data analysis.


---

# Amazon kinesis Data Firehose

### 1. Introduction

- **Amazon Kinesis Data Firehose** is a **fully managed data delivery service** by AWS.    
- It automatically **collects, transforms, and loads streaming data** into destinations such as **S3, Redshift, OpenSearch, or third-party tools** (like Splunk or Datadog).
- Unlike Kinesis Data Streams, Firehose doesn’t require you to manage shards, scaling, or consumers — AWS handles it completely.

---

### 2. Core Concept

- Firehose acts as a **bridge** between **data producers** (applications, IoT devices, logs, etc.) and **storage or analytics services** (S3, Redshift, etc.).
- You just send your data to Firehose, and it delivers it automatically to your chosen destination.

---

### 3. Key Components

| Component                     | Description                                                                         |
| ----------------------------- | ----------------------------------------------------------------------------------- |
| **Producer**                  | The source that sends data (applications, AWS services, IoT sensors).               |
| **Delivery Stream**           | The core Firehose component that defines where data should go.                      |
| **Destination**               | The final target (S3, Redshift, OpenSearch, Splunk, or a custom HTTP endpoint).     |
| **Transformation (optional)** | Firehose can process data using AWS Lambda before delivery.                         |
| **Buffering**                 | Firehose temporarily buffers incoming data before delivery (based on size or time). |

---

### 4. Data Flow

1. Producers send streaming data to **Firehose Delivery Stream**.    
2. Firehose buffers the data (to improve efficiency).
3. Optionally, Firehose invokes a **Lambda function** to transform or filter the data.
4. Firehose automatically **compresses, encrypts, and delivers** the data to the destination.

---

### 5. Buffering

- Firehose buffers incoming data before writing it to the destination.
- You can configure buffering by:
    - **Buffer Size:** 1 MB to 128 MB
    - **Buffer Interval:** 60 to 900 seconds
- Whichever condition is met first (size or time), the data is delivered.
---

### 6. Supported Destinations

Firehose can deliver data to:
- **Amazon S3** – for long-term storage.
- **Amazon Redshift** – for analytics and reporting.
- **Amazon OpenSearch Service** – for search and visualization.
- **Splunk / Datadog / New Relic** – for third-party monitoring tools.
- **Custom HTTP Endpoint** – for your own API or logging system.
---

### 7. Data Transformation

- You can attach an **AWS Lambda function** to transform or enrich data before delivery.
- For example:
    - Convert JSON to CSV.
    - Mask sensitive fields.
    - Add metadata or timestamps

---

### 8. Compression and Encryption

- **Compression:** Supports GZIP, Snappy, or ZIP to reduce storage cost.    
- **Encryption:**
    - At rest: AWS KMS encryption.
    - In transit: SSL/TLS.

---

### 9. Scaling

- Fully managed and **auto-scalable** — no shards or manual scaling required.    
- It automatically adjusts to match the throughput of incoming data.

---

### 10. Error Handling

- If data delivery fails (for example, S3 bucket not available), Firehose automatically retries.    
- It can also route failed records to an **S3 backup bucket** for troubleshooting.

---

### 11. Monitoring

- **CloudWatch metrics** track incoming bytes, delivery success, and throttling.    
- You can enable **data backup to S3** to debug transformation or delivery failures

---

### 12. Pricing

You pay for:
- Amount of **data ingested (per GB)**.
- **Transformation costs** (if Lambda used).
- **Data format conversion** or compression.
- **Data transfer** to destinations.

No cost for shard management — it’s serverless.

---

### 13. Common Use Cases

- Real-time log and metrics streaming from EC2, EKS, or on-prem servers.    
- Continuous delivery of IoT sensor data.
- Loading real-time analytics data into Redshift or OpenSearch.
- Storing application or audit logs directly in S3.
- Centralized monitoring pipelines.

---

### 14. Kinesis Data Streams vs Firehose

| Feature         | **Kinesis Data Streams**           | **Kinesis Data Firehose**                      |
| --------------- | ---------------------------------- | ---------------------------------------------- |
| Management      | Developer-managed (manual scaling) | Fully managed (auto scaling)                   |
| Latency         | Milliseconds                       | 1 to 5 minutes                                 |
| Data Processing | Custom consumers or Lambda         | Lambda transformation only                     |
| Control         | Fine-grained                       | Minimal (automatic delivery)                   |
| Use Case        | Real-time apps, dashboards         | Simple ingestion to storage or analytics tools |

---

### 15. Real-world Example

Imagine your application generates logs every second:

1. Logs are sent to a **Firehose delivery stream**    
2. Firehose buffers and compresses the data.
3. A **Lambda function** adds timestamps and converts it to JSON. 
4. The processed logs are automatically stored in **S3** or indexed in **OpenSearch** for visualization.
---

### 16. Summary

- **Kinesis Data Firehose** automates data ingestion and delivery.    
- No servers or shards to manage — fully managed by AWS.
- Ideal for **log collection**, **streaming analytics**, and **data pipeline automation**.
- Best suited for **real-time to near real-time** use cases where minimal operational effort is preferred.
---

# Amazon MQ
### 1. Introduction

- **Amazon MQ** is a **managed message broker service** provided by AWS.
- It supports **open-source message brokers** like **Apache ActiveMQ** and **RabbitMQ**.
- The purpose of Amazon MQ is to make it easier to **migrate existing message-based applications** to AWS without rewriting them.

---

### 2. Why Amazon MQ Exists

- Many older enterprise systems already use **traditional messaging protocols** (JMS, AMQP, STOMP, MQTT).    
- Services like **SQS/SNS** don’t support these protocols directly.
- **Amazon MQ bridges that gap**  it provides a managed, cloud-based alternative that’s **protocol-compatible** with existing on-prem brokers

---

### 3. Core Concept

- It is a **managed message broker** that handles **message queues, topics, routing, and delivery**.   
- AWS manages the underlying broker infrastructure — including provisioning, patching, and failover
- Applications connect to it using standard messaging APIs and protocols (no code changes needed if you already use ActiveMQ/RabbitMQ).

---

### 4. Supported Brokers
Amazon MQ currently supports:
- **Apache ActiveMQ**
- **RabbitMQ**

You can choose which one based on your system’s needs and compatibility.

---

### 5. Key Features

- **Fully Managed:** AWS handles setup, maintenance, and scaling.    
- **Multi-Protocol Support:** Works with JMS, AMQP, STOMP, MQTT, and WebSocket.
- **High Availability:** Supports active/standby brokers across multiple Availability Zones.
- **Security:**]
    - Encrypted connections (TLS)
	- KMS encryption for messages at rest
    - IAM and broker-level access control    
- **Monitoring:** Integrated with **CloudWatch** for broker metrics.

---

### 6. Components

| Component    | Description                                                 |
| ------------ | ----------------------------------------------------------- |
| **Broker**   | The managed message broker instance (ActiveMQ or RabbitMQ). |
| **Queue**    | Holds messages until a consumer retrieves them.             |
| **Topic**    | Publishes messages to multiple subscribers (pub/sub).       |
| **Producer** | Sends messages to a queue or topic.                         |
| **Consumer** | Receives and processes messages.                            |

---

### 7. Message Flow

1. **Producer** sends a message to a **queue** or **topic**.    
2. The **broker** stores the message until the consumer is ready.
3. **Consumer** retrieves the message.
4. Broker ensures delivery guarantees (persistent or non-persistent) based on configuration.

---

### 8. Deployment Options

- **Single-instance Broker:**    
    - Cheaper, runs in one AZ.
    - Suitable for development or testing.

- **Active/Standby Broker (High Availability):**
    - Two brokers across multiple AZs.
    - Automatic failover and redundancy for production environments.

---

### 9. Security

- Encrypted connections with **TLS**.    
- Message encryption at rest using **AWS KMS**.
- Authentication via **username/password** or **LDAP integration**.
- **IAM policies** for managing who can create, modify, or delete brokers.

---

### 10. Monitoring

- **Amazon CloudWatch** provides metrics like:    
    - Queue size
    - Message count
    - Connection status
    - Throughput
- You can set alarms for thresholds or message backlogs.

---

### 11. Integration

- Works with **EC2, ECS, EKS, Lambda**, and **on-prem** applications.    
- Commonly used to **connect hybrid architectures** — on-prem apps can communicate securely with cloud apps through Amazon MQ.

---

### 12. Use Cases

- Migration of existing **JMS or AMQP-based** messaging systems to AWS.    
- Building **hybrid cloud messaging architectures**.
- Decoupling **legacy enterprise applications**.
- Handling **asynchronous communication** in distributed systems.
- **IoT and event-driven** applications needing protocol compatibility.

---

### 13. Comparison with SQS/SNS

| Feature        | **Amazon MQ**                      | **SQS/SNS**                          |
| -------------- | ---------------------------------- | ------------------------------------ |
| Type           | Managed traditional message broker | Native AWS messaging services        |
| Protocols      | JMS, AMQP, STOMP, MQTT, WebSocket  | AWS proprietary APIs                 |
| Message Order  | Preserved                          | SQS Standard doesn’t guarantee order |
| Delivery Model | Queues & topics (broker-managed)   | SQS = queue, SNS = pub/sub           |
| Use Case       | Legacy system migration            | Cloud-native event-driven apps       |
| Scaling        | Manual (per broker)                | Automatic scaling                    |
| Management     | AWS-managed broker                 | Serverless (no broker)               |

---

### 14. Pricing

- Based on:    
    - **Broker instance hours** (ActiveMQ or RabbitMQ type).
    - **Storage (GB per month)**.
    - **Data transfer** in/out.
- No per-message cost like SQS — you pay for uptime and throughput.
---

### 15. Real-world Example

An enterprise application running on-prem uses **ActiveMQ** for messaging between modules.  
When migrating to AWS:

1. They set up **Amazon MQ for ActiveMQ**.
2. Existing applications connect using the same **JMS URL and credentials**.
3. AWS manages scaling, monitoring, and high availability — no code change needed.

---

### 16. Summary

- **Amazon MQ** provides a managed, cloud-based solution for **traditional message brokers**.    
- Ideal for organizations moving **legacy enterprise systems** to AWS.
- Supports multiple protocols and offers full compatibility with existing apps.
- Best for **hybrid architectures** and **legacy migrations**, not lightweight serverless systems (use SQS/SNS for that).    
