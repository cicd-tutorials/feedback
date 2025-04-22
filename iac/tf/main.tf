provider "kubernetes" {
  ignore_annotations = [
    "^service\\.beta\\.kubernetes\\.io\\/.*load.*balancer.*"
  ]
}

module "feedback_app" {
  source = "./module"

  providers = {
    kubernetes = kubernetes
  }
}

output "url" {
  value = module.feedback_app.url
}
