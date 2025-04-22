provider "kubernetes" {
  # ignore_annotations = [
  #   "^service\\.beta\\.kubernetes\\.io\\/.*load.*balancer.*"
  # ]
}

module "feedback-app" {
  source = "./module"

  providers = {
    kubernetes = kubernetes
  }
}

output "url" {
  value = module.feedback-app.url
}
