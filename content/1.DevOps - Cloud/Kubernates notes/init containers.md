---
title: init containers
tags: [devops---cloud, kubernates-notes]
---
An **Init Container** in Kubernetes is a **special type of container** that runs before the main application containers in a Pod start running. It is primarily used for performing setup tasks that need to be completed before the main containers start execution.

### **Why Use Init Containers?**

1. **Dependency Management:** Ensures that prerequisites (like fetching config files, setting up databases, etc.) are done before starting the main container.
2. **Security:** Keeps initialization tasks separate from the main application, reducing security risks.
3. **Failure Handling:** If an Init Container fails, Kubernetes restarts it until it succeeds, ensuring correct setup.
4. **Resource Optimization:** Allows heavy initialization work to be offloaded from the main application container.

---

### **How Init Containers Work?**

- Init Containers **always run to completion** before the main containers start.
- They **run sequentially**, meaning one Init Container must finish before the next starts.
- If an Init Container fails, Kubernetes **restarts it until it succeeds** or the pod reaches its restart limit.

kubectl edit pod 

![[Pasted image 20250312161125.png]]
