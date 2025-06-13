---
title: Kubernates notes ArgoCD
date: 2025-01-22
---
```
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
```

```
kubectl port-forward svc/argocd-server -n argocd 8080:443
```

```
kubectl get secret argocd-initial-admin-secret -n argocd -o jsonpath="{.data.password}" | base64 -d
```

