# ArgoCD Ingress (HTTP only)
resource "kubernetes_ingress_v1" "argocd" {
  metadata {
    name      = "argocd-server-ingress"
    namespace = "argocd"
    annotations = {
      "kubernetes.io/ingress.class"                 = "nginx"
      "nginx.ingress.kubernetes.io/backend-protocol" = "HTTP"
    }
  }

  spec {
    ingress_class_name = "nginx"

    rule {
      host = var.argocd_host
      http {
        path {
          path      = "/"
          path_type = "Prefix"
          backend {
            service {
              name = "argocd-server"
              port {
                number = 80
              }
            }
          }
        }
      }
    }
  }

  depends_on = [
    helm_release.nginx_ingress,
    helm_release.argocd
  ]
}

# ArgoCD Application for React App
# Using null_resource with kubectl to avoid provider initialization issues during plan
# This approach applies the manifest via kubectl, which doesn't require provider initialization
resource "null_resource" "argocd_application" {
  # Update kubeconfig before applying manifest
  provisioner "local-exec" {
    command = <<-EOT
      aws eks update-kubeconfig --region ${var.aws_region} --name ${module.eks.cluster_name}
      kubectl apply -f - <<EOF
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: vault
  namespace: argocd
spec:
  project: default
  source:
    repoURL: ${var.github_repo_url}
    targetRevision: HEAD
    path: ${var.github_repo_path}
  destination:
    server: https://kubernetes.default.svc
    namespace: app
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
    syncOptions:
    - CreateNamespace=true
EOF
    EOT
  }

  # Re-apply on changes to prevent drift
  triggers = {
    github_repo_url = var.github_repo_url
    github_repo_path = var.github_repo_path
    cluster_name     = module.eks.cluster_name
    cluster_endpoint = module.eks.cluster_endpoint
  }

  depends_on = [
    module.eks,
    helm_release.nginx_ingress,
    helm_release.argocd,
    kubernetes_ingress_v1.argocd
  ]
}

