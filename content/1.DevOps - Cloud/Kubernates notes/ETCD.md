---
title: Kubernates notes ETCD
date: 2025-02-10
---

ETCD is a **distributed key-value store** used to store configuration data, metadata, and distributed system coordination information. It is highly available, consistent, and used extensively in cloud-native applications like **Kubernetes**.

#### **Key Features of ETCD**

- **Strong Consistency:** Uses the **Raft consensus algorithm** to ensure data consistency.
- **High Availability:** Supports leader election and fault tolerance.
- **Lightweight & Fast:** Optimized for read and write performance.
- **Secure:** Supports TLS encryption and authentication.
- **Watch Mechanism:** Clients can subscribe to changes in stored data

#### **How ETCD Works**

- **Nodes (Cluster Members):** ETCD runs on multiple nodes for redundancy.
- **Leader-Follower Model:** One node is elected as the **leader** to handle writes; other nodes **replicate data**.
- **Key-Value Storage:** Data is stored in a simple **key-value** format.


