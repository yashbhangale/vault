# Terraform Commands Reference

Complete guide to all Terraform commands for managing your EKS infrastructure.

## Initial Setup

### Initialize Terraform
```bash
cd terraform
terraform init
```

Downloads and installs required providers (AWS, Kubernetes, Helm, Null).

### Verify Configuration
```bash
terraform validate
```

Checks syntax and configuration without connecting to providers.

### Format Code
```bash
terraform fmt
```

Automatically formats all `.tf` files to follow standard conventions.

## Planning and Applying

### Preview Changes
```bash
terraform plan
```

Shows what Terraform will create, modify, or destroy without making changes.

### Preview with Variables File
```bash
terraform plan -var-file=terraform.tfvars
```

### Save Plan to File
```bash
terraform plan -out=tfplan
```

Saves the plan for later use.

### Apply Changes
```bash
terraform apply
```

Creates/updates infrastructure. Type `yes` when prompted.

### Apply with Auto-approve
```bash
terraform apply -auto-approve
```

Skips confirmation prompt (useful for automation).

### Apply from Saved Plan
```bash
terraform apply tfplan
```

Uses a previously saved plan file.

### Apply Specific Resource
```bash
terraform apply -target=helm_release.nginx_ingress
```

Only applies changes to a specific resource.

## Viewing State

### List All Resources
```bash
terraform state list
```

Shows all resources managed by Terraform.

### Show Resource Details
```bash
terraform state show helm_release.nginx_ingress
terraform state show module.eks
```

Displays detailed information about a specific resource.

### Show All Outputs
```bash
terraform output
```

Lists all output values.

### Show Specific Output
```bash
terraform output cluster_name
terraform output argocd_url
terraform output kubectl_config_command
```

### Refresh State
```bash
terraform refresh
```

Updates state file to match real-world infrastructure without making changes.

## Destroying Infrastructure

### Preview Destroy
```bash
terraform plan -destroy
```

Shows what will be destroyed without actually destroying it.

### Destroy All Resources
```bash
terraform destroy
```

**WARNING:** This will delete your entire EKS cluster and all resources!

### Destroy Specific Resource
```bash
terraform destroy -target=helm_release.argocd
```

Only destroys a specific resource.

### Destroy with Auto-approve
```bash
terraform destroy -auto-approve
```

Skips confirmation prompt.

## Useful Workflow Commands

### Initialize and Apply in One Go
```bash
terraform init && terraform apply
```

### Plan, Save, and Apply
```bash
terraform plan -out=tfplan && terraform apply tfplan
```

### Validate, Format, Plan, and Apply
```bash
terraform fmt && terraform validate && terraform plan && terraform apply
```

### Get Specific Information
```bash
# Get cluster endpoint
terraform output cluster_endpoint

# Get kubectl configuration command
terraform output kubectl_config_command

# Get ArgoCD password command
terraform output argocd_initial_admin_password_command

# Get LoadBalancer info
terraform output nginx_ingress_loadbalancer_info
```

## Advanced Commands

### Import Existing Resource
```bash
terraform import aws_eks_cluster.this cluster-name
```

Imports an existing resource into Terraform state.

### Move Resource in State
```bash
terraform state mv 'old_resource' 'new_resource'
```

Moves a resource to a different location in state file.

### Remove Resource from State
```bash
terraform state rm 'resource'
```

Removes resource from state without destroying it (useful if resource was manually deleted).

### Show State File
```bash
terraform state show
```

Shows entire state file (very long output).

### List Resources by Type
```bash
terraform state list | grep helm
terraform state list | grep module.eks
```

### Force Unlock State
```bash
terraform force-unlock <lock-id>
```

If Terraform state gets locked (e.g., from a crashed apply).

## Troubleshooting Commands

### Verify Provider Versions
```bash
terraform version
```

### Check Provider Compatibility
```bash
terraform providers
```

Lists all providers and their versions.

### Show Required Providers
```bash
terraform providers schema -json | jq
```

### Debug with Verbose Output
```bash
TF_LOG=DEBUG terraform plan
TF_LOG=DEBUG terraform apply
```

Shows detailed debug information (very verbose).

### Check State File Backend
```bash
terraform show -json | jq .backend
```

## Common Workflows

### Complete Setup (First Time)
```bash
cd terraform
terraform init
terraform plan
terraform apply
```

### Update Configuration
```bash
# Edit .tf files, then:
terraform fmt
terraform validate
terraform plan
terraform apply
```

### Check Current State
```bash
terraform refresh
terraform output
terraform state list
```

### Clean Up Everything
```bash
terraform destroy
```

### Update Only Specific Component
```bash
# Example: Update ArgoCD Helm release
terraform plan -target=helm_release.argocd
terraform apply -target=helm_release.argocd
```

## Quick Reference

| Command | Description |
|---------|-------------|
| `terraform init` | Initialize Terraform |
| `terraform plan` | Preview changes |
| `terraform apply` | Apply changes |
| `terraform destroy` | Destroy infrastructure |
| `terraform validate` | Validate configuration |
| `terraform fmt` | Format code |
| `terraform refresh` | Refresh state |
| `terraform output` | Show outputs |
| `terraform state list` | List all resources |
| `terraform state show <resource>` | Show resource details |

## Environment Variables

You can also set variables via environment variables:

```bash
export TF_VAR_aws_region=eu-north-1
export TF_VAR_cluster_name=20api-eks
terraform plan
```

## Working with Workspaces (Optional)

```bash
# Create a new workspace (e.g., for staging)
terraform workspace new staging

# List workspaces
terraform workspace list

# Switch workspace
terraform workspace select staging

# Show current workspace
terraform workspace show
```

## Best Practices

1. **Always run `terraform plan` before `terraform apply`**
2. **Review the plan carefully before applying**
3. **Save important plans**: `terraform plan -out=tfplan`
4. **Use `terraform fmt` regularly** to keep code formatted
5. **Run `terraform validate`** to catch errors early
6. **Use version control** for your Terraform files
7. **Backup state file** if using local backend
8. **Use remote state** (S3) for team collaboration

## State File Management

### Local State (Current Setup)
- State file: `terraform.tfstate`
- Backup: `terraform.tfstate.backup`

### View State File
```bash
cat terraform.tfstate
```

### Backup State Manually
```bash
cp terraform.tfstate terraform.tfstate.backup.$(date +%Y%m%d)
```

## Quick Troubleshooting

### If `terraform init` fails:
```bash
# Remove .terraform directory and reinit
rm -rf .terraform
terraform init
```

### If state is out of sync:
```bash
terraform refresh
```

### If plan shows unexpected changes:
```bash
# Compare state with reality
terraform refresh
terraform plan
```

### If apply fails partway:
```bash
# Terraform automatically saves state, just run apply again
terraform apply
```

## Integration with kubectl

After Terraform creates the cluster:

```bash
# Get kubectl config command from Terraform
terraform output kubectl_config_command

# Run it
aws eks update-kubeconfig --region eu-north-1 --name 20api-eks

# Verify connection
kubectl get nodes
```

## Example Daily Workflow

```bash
# 1. Navigate to terraform directory
cd terraform

# 2. Check current state
terraform state list

# 3. View outputs
terraform output

# 4. Make changes to .tf files (if needed)
# nano variables.tf

# 5. Format and validate
terraform fmt
terraform validate

# 6. Preview changes
terraform plan

# 7. Apply if changes look good
terraform apply

# 8. Get updated outputs
terraform output
```

