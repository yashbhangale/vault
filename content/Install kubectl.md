---
title: Install kubectl
---

```bash
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
```


```bash
chmod +x kubectl
```


```bash
sudo mv kubectl /usr/local/bin/
```

```bash
kubectl version --client
```

```bash
kubectl get po
```

