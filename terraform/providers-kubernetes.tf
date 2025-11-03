# Kubernetes and Helm providers configured using exec plugin
# Using module outputs directly to avoid circular dependencies
# The exec plugin handles authentication dynamically at runtime via AWS CLI
# 
# IMPORTANT: During 'terraform plan', you may see "cannot create REST client" warnings.
# This is EXPECTED and NOT a blocker - the provider will work correctly during 'terraform apply'
# when the cluster exists.
#
# This works because:
# 1. manage_aws_auth_configmap = false means EKS module doesn't need Kubernetes provider
# 2. Module outputs don't create dependencies - they're computed values
# 3. Exec plugin fetches tokens dynamically at runtime using AWS CLI
# 4. During apply, values become available as resources are created

provider "kubernetes" {
  host                   = module.eks.cluster_endpoint
  cluster_ca_certificate = base64decode(module.eks.cluster_certificate_authority_data)
  
  exec {
    api_version = "client.authentication.k8s.io/v1beta1"
    command     = "aws"
    args = [
      "eks",
      "get-token",
      "--cluster-name",
      module.eks.cluster_name,
      "--region",
      var.aws_region
    ]
    env = {}
  }
}

provider "helm" {
  kubernetes {
    host                   = module.eks.cluster_endpoint
    cluster_ca_certificate = base64decode(module.eks.cluster_certificate_authority_data)
    
    exec {
      api_version = "client.authentication.k8s.io/v1beta1"
      command     = "aws"
      args = [
        "eks",
        "get-token",
        "--cluster-name",
        module.eks.cluster_name,
        "--region",
        var.aws_region
      ]
      env = {}
    }
  }
}

