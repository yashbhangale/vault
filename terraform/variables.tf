variable "aws_region" {
  description = "AWS region for EKS cluster"
  type        = string
  default     = "eu-north-1"
}

variable "cluster_name" {
  description = "Name of the EKS cluster"
  type        = string
  default     = "20api-eks"
}

variable "node_instance_type" {
  description = "EC2 instance type for EKS node group"
  type        = string
  default     = "t3.medium"
}

variable "node_desired_capacity" {
  description = "Desired number of nodes in the node group"
  type        = number
  default     = 1
}

variable "node_min_capacity" {
  description = "Minimum number of nodes in the node group"
  type        = number
  default     = 1
}

variable "node_max_capacity" {
  description = "Maximum number of nodes in the node group"
  type        = number
  default     = 1
}

variable "cluster_version" {
  description = "Kubernetes version for EKS cluster"
  type        = string
  default     = "1.28"
}

variable "github_repo_url" {
  description = "GitHub repository URL for the React app (used by ArgoCD Application)"
  type        = string
  default     = "https://github.com/yashbhangale/vault.git"
}

variable "github_repo_path" {
  description = "Path inside the repo where Kubernetes manifests are located"
  type        = string
  default     = "kubernetes"
}

variable "domain_name" {
  description = "Domain name for the application"
  type        = string
  default     = "20api.com"
}

variable "argocd_host" {
  description = "Hostname for ArgoCD ingress"
  type        = string
  default     = "argo.20api.com"
}

variable "tags" {
  description = "Tags to apply to all resources"
  type        = map(string)
  default = {
    Project = "20api"
    ManagedBy = "Terraform"
  }
}

