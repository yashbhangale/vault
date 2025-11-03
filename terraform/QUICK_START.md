# Quick Start Guide

## Prerequisites Check

```bash
# Check AWS credentials
aws sts get-caller-identity

# Check Terraform version
terraform version  # Should be >= 1.2.0

# Check kubectl
kubectl version --client
```

## Step-by-Step Setup

### 1. Initialize Terraform

```bash
cd terraform
terraform init
```

### 2. Review Variables

Edit `terraform.tfvars` or copy from example:

```bash
cp terraform.tfvars.example terraform.tfvars
# Edit terraform.tfvars with your values
```

### 3. Plan

```bash
terraform plan
```

### 4. Apply

```bash
terraform apply
# Type 'yes' when prompted
```

**Wait time:** ~15-20 minutes

### 5. Configure kubectl

```bash
aws eks update-kubeconfig --region eu-north-1 --name 20api-eks
kubectl get nodes
```

### 6. Get LoadBalancer Address

```bash
kubectl get svc -n ingress-nginx ingress-nginx-controller
```

Copy the `EXTERNAL-IP` or `EXTERNAL-HOSTNAME`.

### 7. Configure DNS

In Hostinger (or your DNS provider):

- **A Record** or **CNAME** for `20api.com` and `www.20api.com` → [LoadBalancer IP/Hostname]
- **CNAME** for `argocd.20api.com` → [LoadBalancer Hostname]

### 8. Get ArgoCD Password

```bash
kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 --decode
```

### 9. Access ArgoCD

- URL: `https://argocd.20api.com` (or `http://` if TLS not configured)
- Username: `admin`
- Password: [from step 8]

### 10. Verify App Deployment

```bash
# Check ArgoCD application
kubectl get applications -n argocd

# Check app pods
kubectl get pods -n app

# Check app ingress
kubectl get ingress -n app
```

Access your app at `https://20api.com` after DNS propagation.

## Troubleshooting

### Cluster creation fails
```bash
# Check AWS permissions
aws iam get-user
aws eks describe-cluster --name 20api-eks --region eu-north-1
```

### kubectl connection fails
```bash
# Reconfigure kubectl
aws eks update-kubeconfig --region eu-north-1 --name 20api-eks --force

# Test connection
kubectl get nodes
```

### ArgoCD not syncing
```bash
# Check ArgoCD logs
kubectl logs -n argocd -l app.kubernetes.io/name=argocd-server

# Check application status
kubectl describe application vault -n argocd
```

### DNS not working
- Wait 5-15 minutes for DNS propagation
- Verify DNS records point to correct LoadBalancer
- Test with: `nslookup 20api.com` and `nslookup argocd.20api.com`

## Common Commands

```bash
# View all outputs
terraform output

# Check cluster status
kubectl cluster-info

# View all resources
kubectl get all -A

# Check ingress controller
kubectl get pods -n ingress-nginx

# Check ArgoCD
kubectl get pods -n argocd
```

## Cleanup

```bash
# Destroy everything
terraform destroy

# Or destroy specific resources
terraform destroy -target=module.eks
```

