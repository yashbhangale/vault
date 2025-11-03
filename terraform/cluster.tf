# VPC and Networking
data "aws_availability_zones" "available" {
  state = "available"
}

module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "~> 5.0"

  name = "${var.cluster_name}-vpc"
  cidr = "10.0.0.0/16"

  azs             = slice(data.aws_availability_zones.available.names, 0, 2)
  private_subnets = ["10.0.1.0/24", "10.0.2.0/24"]
  public_subnets  = ["10.0.101.0/24", "10.0.102.0/24"]

  enable_nat_gateway   = true
  single_nat_gateway   = true
  enable_dns_hostnames = true
  enable_dns_support   = true

  public_subnet_tags = {
    "kubernetes.io/role/elb" = "1"
    "kubernetes.io/cluster/${var.cluster_name}" = "shared"
  }

  private_subnet_tags = {
    "kubernetes.io/role/internal-elb" = "1"
    "kubernetes.io/cluster/${var.cluster_name}" = "shared"
  }

  tags = var.tags
}

# EKS Cluster
module "eks" {
  source  = "terraform-aws-modules/eks/aws"
  version = "~> 19.0"

  cluster_name    = var.cluster_name
  cluster_version = var.cluster_version

  vpc_id     = module.vpc.vpc_id
  subnet_ids = module.vpc.private_subnets

  cluster_endpoint_public_access = true

  # Enable IAM OIDC Provider for service accounts
  enable_irsa = true

  # Enable managed aws-auth ConfigMap - required for nodes to join cluster
  # This is safe now because we use module outputs directly in provider config
  # (no circular dependency since module outputs are computed values)
  manage_aws_auth_configmap = true

  # EKS Managed Node Groups
  eks_managed_node_groups = {
    default = {
      desired_size = var.node_desired_capacity
      min_size     = var.node_min_capacity
      max_size     = var.node_max_capacity

      instance_types = [var.node_instance_type]

      # Use Amazon Linux 2023 (AL2023) instead of deprecated AL2
      # AL2 AMIs are deprecated after November 26, 2025
      # AL2023 provides: secure-by-default, SELinux, IMDSv2-only, faster boot times
      ami_type = "AL2023_x86_64_STANDARD"

      # Enable launch template
      use_custom_launch_template = false

      # Disk configuration
      disk_size = 20

      # Tags
      tags = var.tags
    }
  }

  tags = var.tags
}

# Data source for AWS account ID (used elsewhere if needed)
data "aws_caller_identity" "current" {}

