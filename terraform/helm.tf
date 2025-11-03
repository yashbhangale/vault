# NGINX Ingress Controller
resource "helm_release" "nginx_ingress" {
  name       = "nginx-ingress"
  repository = "https://kubernetes.github.io/ingress-nginx"
  chart      = "ingress-nginx"
  version    = "4.8.3"

  namespace        = "ingress-nginx"
  create_namespace = true

  values = [yamlencode({
    controller = {
      service = {
        type                        = "LoadBalancer"
        annotations                 = {}
        externalTrafficPolicy       = "Cluster"
        preserveSourceIP            = false
      }
      replicaCount = 1
      resources = {
        requests = {
          cpu    = "100m"
          memory = "128Mi"
        }
        limits = {
          cpu    = "200m"
          memory = "256Mi"
        }
      }
    }
  })]

  timeout = 600

  depends_on = [module.eks]
}

# ArgoCD
resource "helm_release" "argocd" {
  name       = "argocd"
  repository = "https://argoproj.github.io/argo-helm"
  chart      = "argo-cd"
  version    = "6.7.18"

  namespace        = "argocd"
  create_namespace = true

  values = [yamlencode({
    server = {
      extraArgs = []
      service = {
        type = "ClusterIP"
      }
      ingress = {
        enabled = false # We'll create ingress via Kubernetes manifest
      }
    }
    controller = {
      replicaCount = 1
    }
    repoServer = {
      replicaCount = 1
    }
    applicationSet = {
      replicaCount = 1
    }
    rbac = {
      create = true
    }
    configs = {
      params = {
        "server.insecure" = true  # Enable HTTP access
      }
    }
  })]

  timeout = 600

  depends_on = [module.eks]
}

