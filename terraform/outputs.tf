output "cluster_id" {
  description = "EKS cluster ID"
  value       = module.eks.cluster_id
}

output "cluster_name" {
  description = "EKS cluster name"
  value       = module.eks.cluster_name
}

output "cluster_endpoint" {
  description = "Endpoint for EKS control plane"
  value       = module.eks.cluster_endpoint
}

output "cluster_security_group_id" {
  description = "Security group ID attached to the EKS cluster"
  value       = module.eks.cluster_security_group_id
}

output "cluster_certificate_authority_data" {
  description = "Base64 encoded certificate data required to communicate with the cluster"
  value       = module.eks.cluster_certificate_authority_data
}

output "kubectl_config_command" {
  description = "Command to configure kubectl to use this EKS cluster"
  value       = "aws eks update-kubeconfig --region ${var.aws_region} --name ${module.eks.cluster_name}"
}

output "nginx_ingress_loadbalancer_info" {
  description = "Instructions to get NGINX Ingress Controller LoadBalancer hostname"
  value       = "Run: kubectl get svc -n ingress-nginx ingress-nginx-controller -o jsonpath='{.status.loadBalancer.ingress[0].hostname}'"
}

output "argocd_initial_admin_password_command" {
  description = "Command to get ArgoCD initial admin password"
  value       = "kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath=\"{.data.password}\" | base64 --decode"
}

output "argocd_url" {
  description = "ArgoCD server URL"
  value       = "http://${var.argocd_host}"
}

output "app_url" {
  description = "Application URL"
  value       = "http://${var.domain_name}"
}

