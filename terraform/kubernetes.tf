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
# Using kubernetes_manifest now that cluster exists
resource "kubernetes_manifest" "argocd_application" {
  manifest = {
    apiVersion = "argoproj.io/v1alpha1"
    kind       = "Application"
    metadata = {
      name      = "vault"
      namespace = "argocd"
    }
    spec = {
      project = "default"
      source = {
        repoURL        = var.github_repo_url
        targetRevision = "HEAD"
        path           = var.github_repo_path
      }
      destination = {
        server    = "https://kubernetes.default.svc"
        namespace = "app"
      }
      syncPolicy = {
        automated = {
          prune    = true
          selfHeal = true
        }
        syncOptions = ["CreateNamespace=true"]
      }
    }
  }

  depends_on = [
    module.eks,
    helm_release.nginx_ingress,
    helm_release.argocd,
    kubernetes_ingress_v1.argocd
  ]
}

