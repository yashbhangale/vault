---
title: "Cka Questions"
tags:
  - "cloud-devops"
type: "reference"
area: "cloud-devops"
topic: "CKA"
status: "unreviewed"
source: "obsidian"
---

# A pod stuck in pending state how can you debug it  or troubleshoot it 

- kubectl get po <po-name>
- kubectl describe po <po-name>

check event section at the btm of describe

causes : insufficient memory
node selector and node affinity
taints without matching tolleration
no available node
	pvc not bound

eg : kubectl describe po nginx 

if you see
0/3 available, insufficient cpu 

the schedullar cannot find pod with enough cpu , so the pod remains pending

---

# A pod is in running state , but you cannot access the application through k8s service, how to troubleshoot it ??

> check service 
- kubectl get svc
- kubectl describe svc (service name)

> check whether service has any endpoints 
- kubectl get endpoints <svc-name>
> if endpoints is empty checks labels 
- kubectl get pods --show-labels

Then compare it with service selector

- kubectl describe service <service-name>

> **Most common cause :** service selector does'nt match pod labels.

Eg:

```
# Service
selector:
  app: nginx

# Pod
labels:
  app: apache
```

-> no matching po --> no endpoints --> service does'nt route traffic...

---

# A pod is in CrashLoopBackoff state. How do you troubleshoot it ?

- kubectl get pod <pod>
- kubectl describe pod <pod>
- kubectl log <pod>
- kubectl log <pod> --previous

key thing --previous is impt coz container is always crashed

check for 

- Application errors
- wrong command/arguments
- Missing Config/Secret
- Missing env vars
- OOMKilled
- Failed health probes

Example :

- kubectl logs nginx --previous

if you see OOMKilled -> container exceeded its memory limit.

shortcuts : CrashLoopBackoff --> logs + describe + previous logs 

---



