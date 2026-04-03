---
title: Backend
tags: [devops---cloud, backend]
---
Source : https://youtu.be/fkQUkZRFq8g

## **Backend & System Design Notes**

### **1. It’s All About Data**

Everything in backend and system design revolves around **how data flows, is processed, and is stored**.  
You need to handle **data integrity, access patterns, scaling, and reliability** efficiently.

---

### **2. Request-Response Cycle**

- **Request (Req)**: Sent by the client (frontend, mobile app, etc.) to the server.
- **Response (Res)**: Sent by the server after processing the request.
- Understand how middleware, routing, and controllers fit into this cycle.

---

### **3. Validation**

- Validate incoming data before processing or storing it in the database.
- Types:
    - **Client-side** (basic checks)
    - **Server-side** (final authority)
- Helps maintain data consistency and prevents malicious input.

---

### **4. Routing**

- Determines which controller or service handles a given request.
- Example: `/api/users` → `UserController`
- Can include middleware for authentication, logging, or validation.

---

### **5. Database Fundamentals**

- **Database Design (DB Design)**:
    - **Normalization**: Reduce redundancy, ensure data integrity.
    - **Denormalization**: Improve performance for read-heavy systems.
- **Indexes**:
    - Speed up query performance by optimizing lookups.
    - Be careful with **“stupid indexes”** — too many or unnecessary indexes slow down writes.
- **Sharding**:
    - Splitting data across multiple databases or servers.
    - Useful for **horizontal scaling** when data volume grows.
- **Replication**:
    - Copying data across servers to increase availability and reliability.

---

### **6. Scaling**

- **Vertical Scaling**: Add more power (CPU, RAM) to a single server.
- **Horizontal Scaling**: Add more servers to distribute load.
- Use **load balancers** to distribute incoming requests efficiently.
- **Queues**:
    - Used when your system can’t process all requests immediately.
    - Hold requests temporarily and process them asynchronously (e.g., with RabbitMQ, Kafka, SQS).

---

### **7. Caching & Prewarming**

- **Caching**: Store frequently accessed data in-memory (Redis, Memcached) for fast retrieval.
- **Pre-caching / Pre-warming**:
    - Load cache or initialize backend/database servers before traffic peaks.
    - Reduces cold-start latency.

---

### **8. Rate Limiting**

- Protects the server from being overwhelmed by too many requests.
- Common strategies:
    - **Token bucket**
    - **Leaky bucket**
    - **Fixed window / Sliding window**
- Often implemented using Redis or API gateways (e.g., NGINX, Kong).

---

### **9. Event-Driven Architecture**

- System reacts to events instead of direct requests.
- Uses **Pub/Sub model**:
    - **Publisher** emits events.
    - **Subscriber** listens and reacts.
- Improves scalability, decouples services.
- Tools: Kafka, RabbitMQ, AWS SNS/SQS.

---

### **10. Command Query Separation (CQS)**

- A design principle stating:
    - **Commands** change the system state (e.g., create/update data).
    - **Queries** retrieve data but don’t modify it.
- Improves clarity and maintainability.

---

### **11. Prebound / Prewarmed Servers**

- Keep backend or database connections ready to handle incoming traffic.
- Reduces connection overhead and improves response time.
- Common in high-performance APIs and serverless setups.

---

### **12. System Design Principles**

- **Scalability**: System can handle increased load.
- **Availability**: System remains operational even when components fail.
- **Reliability**: System consistently delivers correct results.
- **Consistency**: Data remains accurate across replicas.
- **Observability**: Use logs, metrics, and tracing to monitor the system.

---

### **13. Papalism (Possibly Meant “Parallelism”)**

- **Parallelism**: Multiple tasks processed simultaneously to improve performance.
- Often combined with **concurrency** to maximize resource utilization.

---

### **14. Bonus Concepts to Add**

To make your notes more complete:

- **Load Balancing**: Distribute traffic among multiple servers.
- **CDN (Content Delivery Network)**: Cache static files close to users.
- **API Gateway**: Manage, secure, and route API calls.
- **Microservices**: Split large systems into smaller, independent services.
- **Monitoring & Logging**: Tools like Prometheus, Grafana, SigNoz for observability.
