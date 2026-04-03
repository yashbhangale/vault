---
title: cluster maintainance
tags: [devops---cloud, kubernates-notes]
---
operating system upgrade 
```
kubectl drain node-1
kubectl cordon node-2
kubectl uncordon node-1
```


In Kubernetes, commands like `drain`, `cordon`, and `uncordon` are used during maintenance to manage the scheduling of pods on nodes. Here's a brief explanation:

1. **`kubectl drain node-1`**:
    - Marks the node as **unschedulable** (like cordoning) and evicts all the pods from the node to prepare for maintenance.
    - Ensures no new pods are scheduled on the node.
    - Pods that are part of a Deployment, ReplicaSet, etc., are rescheduled to other available nodes.
    - Ideal for safe maintenance of the node (e.g., upgrades, patches).

2. **`kubectl cordon node-2`**:    
    - Marks the node as **unschedulable** without evicting any running pods.
    - Prevents new pods from being scheduled on the node, but existing ones remain running.
    - Useful when you want to stop further scheduling without interrupting current workloads.

3. **`kubectl uncordon node-1`**:
    - **Makes the node schedulable** again, allowing new pods to be placed on the node.
    - Used after maintenance is complete and the node is ready to rejoin the cluster.

### Real-world use cases:

- Draining a node is used during planned maintenance, upgrades, or troubleshooting to move workloads safely.
- Cordoning is often used when you want to test or perform changes on a node without impacting currently running services.
- Uncordoning allows the node to start receiving new workloads after maintenance is done.




# To unschedule nodes use command

```
kubectl drain node01 --ignore-daemonsets
```

