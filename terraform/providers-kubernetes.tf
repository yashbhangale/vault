# Kubernetes and Helm providers configured using exec plugin
# Using module outputs directly (not data sources) to avoid circular dependency
# The exec plugin will handle authentication, and module outputs provide cluster info
# This works because:
# 1. manage_aws_auth_configmap = false means EKS module doesn't need Kubernetes provider
# 2. Module outputs are available after cluster creation
# 3. Exec plugin fetches tokens dynamically at runtime

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

