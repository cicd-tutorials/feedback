variable "namespace" {
  type    = string
  default = "three-tier-example-app"
}

provider "kubernetes" {}

data "kubernetes_nodes" "this" {}

locals {
  addresses   = data.kubernetes_nodes.this.nodes[0].status[0].addresses
  external_ip = local.addresses[index(local.addresses.*.type, "ExternalIP")].address
}

resource "kubernetes_namespace" "this" {
  metadata {
    name = var.namespace
  }
}

resource "kubernetes_deployment" "api" {
  metadata {
    name      = "api"
    namespace = var.namespace
    labels = {
      app = "api"
    }
  }

  spec {
    selector {
      match_labels = {
        app = "api"
      }
    }

    template {
      metadata {
        labels = {
          app = "api"
        }
      }

      spec {
        container {
          image = "ghcr.io/kangasta/three-tier-example-app-api:6"
          name  = "api"

          env {
            name  = "DB_URL"
            value = "postgresql://user:pass@db:5432/feedback"
          }
        }
      }
    }
  }
}

resource "kubernetes_service" "api" {
  metadata {
    name      = "api"
    namespace = var.namespace
  }
  spec {
    selector = {
      app = "api"
    }

    port {
      port        = 80
      target_port = 8000
    }

    type = "NodePort"
  }
}

resource "kubernetes_config_map" "ui" {
  metadata {
    name      = "ui"
    namespace = var.namespace
  }
  data = {
    config = "const serverUrl = \"http://${local.external_ip}:${kubernetes_service.api.spec[0].port[0].node_port}\";"
  }
  depends_on = [kubernetes_service.api]
}

resource "kubernetes_deployment" "ui" {
  metadata {
    name      = "ui"
    namespace = var.namespace
    labels = {
      app = "ui"
    }
  }

  spec {
    selector {
      match_labels = {
        app = "ui"
      }
    }

    template {
      metadata {
        labels = {
          app = "ui"
        }
      }

      spec {
        container {
          image = "ghcr.io/kangasta/three-tier-example-app-ui:6"
          name  = "ui"
          volume_mount {
            name       = "ui"
            mount_path = "/usr/share/nginx/html/config.js"
            sub_path   = "config"
          }
        }

        volume {
          name = "ui"
          config_map {
            name = "ui"
          }
        }
      }
    }
  }
}

resource "kubernetes_service" "ui" {
  metadata {
    name      = "ui"
    namespace = var.namespace
  }
  spec {
    selector = {
      app = "ui"
    }

    port {
      port        = 80
      target_port = 80
    }

    type = "NodePort"
  }
}

resource "kubernetes_deployment" "db" {
  metadata {
    name      = "db"
    namespace = var.namespace
    labels = {
      app = "db"
    }
  }

  spec {
    selector {
      match_labels = {
        app = "db"
      }
    }

    template {
      metadata {
        labels = {
          app = "db"
        }
      }

      spec {
        container {
          image = "postgres:14"
          name  = "db"

          env {
            name  = "POSTGRES_USER"
            value = "user"
          }

          env {
            name  = "POSTGRES_PASSWORD"
            value = "pass"
          }

          env {
            name  = "POSTGRES_DB"
            value = "feedback"
          }
        }
      }
    }
  }
}

resource "kubernetes_service" "db" {
  metadata {
    name      = "db"
    namespace = var.namespace
  }
  spec {
    selector = {
      app = "db"
    }

    port {
      port        = 5432
      target_port = 5432
    }
  }
}

output "ui_url" {
  value = "http://${local.external_ip}:${kubernetes_service.ui.spec[0].port[0].node_port}"
}
