# Terraform Infrastructure for EKS Cluster with ArgoCD

This Terraform configuration sets up a complete DevSecOps pipeline infrastructure on AWS EKS:

- **EKS Cluster** in `eu-north-1` region with a single `t3.medium` node
- **NGINX Ingress Controller** installed via Helm
- **ArgoCD** installed via Helm for GitOps deployments
- **ArgoCD Application** configured to deploy your React app from GitHub

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     AWS EKS Cluster                          │
│                                                               │
│  ┌──────────────────┐         ┌──────────────────┐          │
│  │  NGINX Ingress   │         │     ArgoCD       │          │
│  │   Controller     │────────▶│     Server       │          │
│  └──────────────────┘         └──────────────────┘          │
│         │                               │                    │
│         │                               │                    │
│         ▼                               ▼                    │
│  ┌──────────────────┐         ┌──────────────────┐          │
│  │  20api.com       │         │ argocd.20api.com │          │
│  │  React App       │         │  ArgoCD UI       │          │
│  └──────────────────┘         └──────────────────┘          │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

## Prerequisites

1. **AWS Account** with appropriate permissions
2. **AWS CLI** configured with credentials:
   ```bash
   aws configure
   ```
   Or set environment variables:
   ```bash
   export AWS_ACCESS_KEY_ID=your_access_key
   export AWS_SECRET_ACCESS_KEY=your_secret_key
   ```
3. **Terraform** installed (>= 1.2.0)
4. **kubectl** installed
5. **helm** installed (optional, for manual operations)

## File Structure

```
terraform/
├── providers.tf      # Terraform providers configuration
├── variables.tf      # Variable definitions
├── cluster.tf        # EKS cluster and VPC setup
├── helm.tf           # Helm chart installations (NGINX, ArgoCD)
├── kubernetes.tf     # Kubernetes resources (Ingress, ArgoCD Application)
├── outputs.tf        # Output values
└── README.md         # This file
```

## Quick Start

### 1. Initialize Terraform

```bash
cd terraform
terraform init
```

### 2. Review and Customize Variables

Edit `variables.tf` or create a `terraform.tfvars` file:

```hcl
aws_region           = "eu-north-1"
cluster_name         = "20api-eks"
node_instance_type   = "t3.medium"
node_desired_capacity = 1
domain_name          = "20api.com"
argocd_host          = "argocd.20api.com"
github_repo_url      = "https://github.com/yashbhangale/vault.git"
github_repo_path     = "kubernetes"
```

### 3. Plan the Infrastructure

```bash
terraform plan
```

Review the planned changes carefully.

### 4. Apply the Infrastructure

**Important:** Due to provider initialization requirements, the infrastructure must be applied in two stages:

#### Stage 1: Create the EKS Cluster

First, create the EKS cluster and VPC:

```bash
terraform apply -target=module.eks -target=module.vpc -target=data.aws_eks_cluster.cluster -target=data.aws_eks_cluster_auth.cluster
```

Type `yes` when prompted. This will take approximately 10-15 minutes.

#### Stage 2: Apply Remaining Resources

After the cluster is created, apply the remaining resources (Helm charts and Kubernetes manifests):

```bash
terraform apply
```

Type `yes` when prompted. This will take approximately 5-10 minutes.

**Alternative:** If you prefer a single command (may show plan-time warnings but will work during apply):

```bash
terraform apply -auto-approve
```

**Note:** Total time is approximately 15-20 minutes.

### 5. Configure kubectl

After Terraform completes, configure kubectl:

```bash
aws eks update-kubeconfig --region eu-north-1 --name 20api-eks
```

Verify connection:

```bash
kubectl get nodes
```

### 6. Get NGINX Ingress LoadBalancer Address

```bash
kubectl get svc -n ingress-nginx ingress-nginx-controller
```

Note the `EXTERNAL-IP` or `EXTERNAL-HOSTNAME` value.

### 7. Configure DNS Records

In your DNS provider (Hostinger):

#### Option A: Using A Record (if LoadBalancer provides static IP)
- **Type:** A
- **Name:** `@` (or root)
- **Value:** [LoadBalancer IP]
- **TTL:** 300

- **Type:** A
- **Name:** `www`
- **Value:** [LoadBalancer IP]
- **TTL:** 300

- **Type:** CNAME
- **Name:** `argocd`
- **Value:** [LoadBalancer hostname]
- **TTL:** 300

#### Option B: Using CNAME (Recommended for subdomains)
- **Type:** CNAME
- **Name:** `www`
- **Value:** [LoadBalancer hostname]
- **TTL:** 300

- **Type:** CNAME
- **Name:** `argocd`
- **Value:** [LoadBalancer hostname]
- **TTL:** 300

**Important:** Most DNS providers don't allow CNAME at the apex (root domain). For production, consider:
- Using Route53 with Alias records (recommended)
- Using Cloudflare with CNAME flattening
- Using A records (not recommended as LoadBalancer IP can change)

### 8. Get ArgoCD Admin Password

```bash
kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 --decode
```

The default username is `admin`.

### 9. Access ArgoCD

1. Wait for DNS propagation (usually 5-15 minutes)
2. Navigate to `https://argocd.20api.com` (or `http://` if TLS is not configured)
3. Login with:
   - **Username:** `admin`
   - **Password:** [password from step 8]

### 10. Verify Application Deployment

The ArgoCD Application should automatically sync and deploy your React app. Check:

```bash
kubectl get applications -n argocd
kubectl get pods -n app
kubectl get ingress -n app
```

Access your app at `https://20api.com` after DNS propagation.

## Outputs

After `terraform apply`, useful outputs are displayed:

- `cluster_id`: EKS cluster ID
- `cluster_endpoint`: EKS API endpoint
- `kubectl_config_command`: Command to configure kubectl
- `argocd_url`: ArgoCD server URL
- `app_url`: Application URL
- `argocd_initial_admin_password_command`: Command to get ArgoCD password

To see all outputs:

```bash
terraform output
```

## Customization

### Change Node Instance Type

Edit `variables.tf` or create `terraform.tfvars`:

```hcl
node_instance_type = "t3.large"
```

### Scale Nodes

```hcl
node_desired_capacity = 2
node_min_capacity     = 1
node_max_capacity     = 3
```

### Change Kubernetes Version

```hcl
cluster_version = "1.29"
```

### Update GitHub Repository

```hcl
github_repo_url  = "https://github.com/your-username/your-repo.git"
github_repo_path = "kubernetes"
```

## Troubleshooting

### Kubernetes Provider Error: "cannot create REST client: no client config"

This error occurs during `terraform plan` because the Kubernetes provider cannot initialize without an existing cluster. This is expected behavior.

**Solution:** Apply the infrastructure in two stages (see Step 4 in Quick Start):
1. First apply to create the EKS cluster
2. Then apply the remaining resources

The error will resolve once the cluster exists after the first apply stage.

### Cluster Creation Fails

- Check AWS credentials: `aws sts get-caller-identity`
- Verify IAM permissions
- Check region availability

### kubectl Connection Issues

```bash
# Verify kubeconfig
kubectl config current-context

# Reconfigure
aws eks update-kubeconfig --region eu-north-1 --name 20api-eks
```

### ArgoCD Application Not Syncing

1. Check ArgoCD UI for errors
2. Verify repository access:
   ```bash
   kubectl describe application vault -n argocd
   ```
3. Check if namespace exists:
   ```bash
   kubectl get namespace app
   ```

### Ingress Not Working

1. Check NGINX ingress controller:
   ```bash
   kubectl get pods -n ingress-nginx
   ```
2. Check LoadBalancer status:
   ```bash
   kubectl get svc -n ingress-nginx
   ```
3. Verify DNS records point to LoadBalancer

### TLS/HTTPS Issues

The current setup uses HTTP. To enable HTTPS:

1. Install cert-manager:
   ```bash
   helm repo add jetstack https://charts.jetstack.io
   helm install cert-manager jetstack/cert-manager --namespace cert-manager --create-namespace
   ```

2. Create ClusterIssuer for Let's Encrypt
3. Update ingress annotations with cert-manager annotations

## Cleanup

To destroy all resources:

```bash
terraform destroy
```

**Warning:** This will delete the entire EKS cluster and all associated resources!

## Cost Estimation

Approximate monthly costs (may vary by region):

- EKS Cluster: ~$0.10/hour (~$73/month)
- t3.medium node: ~$0.0416/hour (~$30/month)
- NAT Gateway: ~$0.045/hour (~$32/month)
- LoadBalancer: ~$0.0225/hour (~$16/month)
- Data Transfer: Variable

**Total estimated:** ~$150-200/month

## Security Considerations

1. **IAM Roles**: The EKS module automatically creates appropriate IAM roles
2. **Network Security**: Private subnets for nodes, public subnets for LoadBalancers
3. **ArgoCD Security**: Change default admin password after first login
4. **TLS**: Consider enabling TLS/HTTPS with cert-manager for production
5. **Secrets**: Store sensitive data in Kubernetes Secrets or AWS Secrets Manager

## Additional Resources

- [EKS User Guide](https://docs.aws.amazon.com/eks/latest/userguide/)
- [ArgoCD Documentation](https://argo-cd.readthedocs.io/)
- [NGINX Ingress Controller](https://kubernetes.github.io/ingress-nginx/)
- [Terraform AWS EKS Module](https://registry.terraform.io/modules/terraform-aws-modules/eks/aws/)

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Review Terraform plan output for errors
3. Check Kubernetes and ArgoCD logs
4. Review AWS CloudWatch logs for EKS

