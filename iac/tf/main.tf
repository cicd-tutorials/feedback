provider "kubernetes" {
  ignore_annotations = [
    "^service\\.beta\\.kubernetes\\.io\\/.*load.*balancer.*"
  ]
}

variable "node_port" {
  type    = number
  default = null
}

variable "dns_service" {
  type    = string
  default = "coredns"
}

module "feedback_app" {
  source = "./module"

  providers = {
    kubernetes = kubernetes
  }

  dns_service = var.dns_service
  node_port   = var.node_port
}

output "url" {
  value = module.feedback_app.url
}
