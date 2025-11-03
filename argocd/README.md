# Argo CD setup

This folder installs Argo CD into the `argocd` namespace and exposes the UI at `argocd.20api.com` via the cluster's NGINX Ingress.

## Apply

```bash
# From repo root
kubectl apply -k ./argocd

# Wait for pods
kubectl -n argocd wait --for=condition=Available deployment --all --timeout=300s
```

## Access

- Create a DNS A record in Hostinger for `argocd.20api.com` pointing to your Ingress controller's public IP (or CNAME to your load balancer hostname).
- If you use TLS (recommended), issue a cert and update `ingress-argocd.yaml` tls section.

## Initial admin password

```bash
kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath='{.data.password}' | base64 -d; echo
```

Then log in at `https://argocd.20api.com` (or `http://` if TLS not yet configured) with username `admin`.
