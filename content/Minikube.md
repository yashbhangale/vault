[[Install kubectl]]ls


## 🚀 What is Minikube (1-liner)

Minikube lets you run a **local Kubernetes cluster** on your laptop for learning, testing, and dev work.

---

## 🔧 Installation Check

```bash
minikube version
kubectl version --client
```

If both work → you’re good.

---

## ▶️ Start & Stop Minikube

```bash
minikube start
```

Start with specific driver:

```bash
minikube start --driver=docker
```

Stop cluster:

```bash
minikube stop
```

Delete cluster (reset everything):

```bash
minikube delete
```

Check status:

```bash
minikube status
```

---

## 🧠 Basic Cluster Info

```bash
kubectl cluster-info
kubectl get nodes
kubectl get pods -A
```

---

## 📦 Deploy Your First App

Example: nginx

```bash
kubectl create deployment nginx --image=nginx
```

Check deployment:

```bash
kubectl get deployments
kubectl get pods
```

Expose app:

```bash
kubectl expose deployment nginx --type=NodePort --port=80
```

Access app:

```bash
minikube service nginx
```

---

## 🌐 Services & Networking

List services:

```bash
kubectl get svc
```

Get service URL manually:

```bash
minikube service nginx --url
```

---

## 🔍 Debugging & Logs

Pod logs:

```bash
kubectl logs <pod-name>
```

Describe pod:

```bash
kubectl describe pod <pod-name>
```

Exec into pod:

```bash
kubectl exec -it <pod-name> -- /bin/bash
```

---

## 🧰 Useful Minikube Addons

Enable addons:

```bash
minikube addons enable dashboard
minikube addons enable metrics-server
```

List addons:

```bash
minikube addons list
```

Open dashboard:

```bash
minikube dashboard
```

---

## 🐳 Use Minikube Docker Daemon (Very Important)

So you don’t need Docker Hub for local images 👇

```bash
eval $(minikube docker-env)
```

Now build image:

```bash
docker build -t myapp:latest .
```

Use it in Kubernetes **without pushing**.

---

## 📂 Apply YAML Files

```bash
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
```

Delete resources:

```bash
kubectl delete -f deployment.yaml
```

---

## ⚙️ Scaling & Rollouts

Scale pods:

```bash
kubectl scale deployment nginx --replicas=3
```

Check rollout:

```bash
kubectl rollout status deployment nginx
```

Rollback:

```bash
kubectl rollout undo deployment nginx
```

---

## 🧪 Handy Cheatsheet

```bash
kubectl get all
kubectl get pods -o wide
kubectl delete pod <pod-name>
kubectl delete deployment nginx
```

---

![Image](https://fusionauth.io/img/docs/get-started/download-and-install/kubernetes/fa-minikube.png)

![Image](https://static.abhishek-tiwari.com/old-ghost/images/Dev-Workflow-Local.png)

![Image](https://cdn.thenewstack.io/media/2023/02/d1975006-minikubedash1.jpg)

![Image](https://drek4537l1klr.cloudfront.net/luksa3/v-5/Figures/3.7.png)
