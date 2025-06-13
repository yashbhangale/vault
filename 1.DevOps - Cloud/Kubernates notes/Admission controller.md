---
title: Kubernates notes Admission controller
date: 2025-02-20
---


## **1. What is an Admission Controller?**

🔹 **Admission Controllers** are plugins that **intercept requests** to the Kubernetes API **before** objects are persisted in **etcd**. They **validate and mutate** requests based on policies.

💡 Think of them as **gatekeepers** for Kubernetes objects.

---

## **2. How Admission Controllers Work?**

1️⃣ **User submits a request** (e.g., `kubectl apply -f pod.yaml`)  
2️⃣ **API Server authenticates & authorizes** the request  
3️⃣ **Admission Controllers validate or modify** the request  
4️⃣ **If approved, the object is stored in `etcd`**

⏳ If rejected → The request fails with an error ❌

---

## **3. Types of Admission Controllers**

There are **two types**:

### **🔹 Mutating Admission Controllers**

- Modify requests **before** they are stored
- Example:
    - `MutatingAdmissionWebhook` → Injects sidecars (e.g., Istio)
    - `DefaultStorageClass` → Assigns default storage class

### **🔹 Validating Admission Controllers**

- Only **validate** requests, do not modify
- Example:
    - `ValidatingAdmissionWebhook` → Blocks pods not following policies
    - `PodSecurity` → Enforces security policies

---

## **4. List of Common Admission Controllers**

Some built-in Admission Controllers in Kubernetes:

|**Controller**|**Type**|**Purpose**|
|---|---|---|
|`MutatingAdmissionWebhook`|Mutating|Dynamically modify requests|
|`ValidatingAdmissionWebhook`|Validating|Enforce rules before storing objects|
|`PodSecurity`|Validating|Enforce Pod Security Standards (PSS)|
|`ResourceQuota`|Validating|Enforce resource limits|
|`LimitRanger`|Validating|Apply default resource requests/limits|
|`NodeRestriction`|Validating|Restrict node access to API|
|`DefaultStorageClass`|Mutating|Assigns default storage class|

🔹 The **order** of execution: **Mutating controllers run first**, then **Validating controllers**.

---

## **5. How to Enable/Disable Admission Controllers?**

In **Kube-API Server**, use the `--enable-admission-plugins` flag.

### **Check enabled admission controllers**

```bash
kubectl api-versions | grep admission
```

### **Modify the API Server configuration (For kubeadm clusters)**

1️⃣ Edit the API Server manifest:

```bash
sudo vi /etc/kubernetes/manifests/kube-apiserver.yaml
```

2️⃣ Add/Modify the `--enable-admission-plugins` flag:

```yaml
spec:
  containers:
  - command:
    - kube-apiserver
    - --enable-admission-plugins=PodSecurity,ResourceQuota,LimitRanger
```

3️⃣ Restart the kube-apiserver:

```bash
sudo systemctl restart kubelet
```

---

## **6. Webhook Admission Controllers (Dynamic)**

Instead of static policies, Kubernetes allows **custom Admission Controllers** using **webhooks**.

### **Creating a Mutating Webhook (Example)**

1️⃣ Create a webhook server (e.g., Python, Go)  
2️⃣ Deploy it as a service  
3️⃣ Create a `MutatingWebhookConfiguration` resource  
4️⃣ Kubernetes calls the webhook **before saving the object**

✅ Best for **custom policy enforcement** (e.g., injecting sidecars, enforcing naming conventions)

---

## **7. Best Practices**

✅ Use **Mutating controllers** to **auto-configure** resources  
✅ Use **Validating controllers** to **enforce policies**  
✅ Use **Webhook Admission Controllers** for **custom policies**  
✅ **Test controllers in a dev environment** before enabling in production

---

Let me know if you need examples or help setting up webhooks! 🚀