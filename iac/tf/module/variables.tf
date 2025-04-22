variable "namespace" {
  type    = string
  default = "feedback"
}

variable "dns_service" {
  type    = string
  default = "coredns"
}

variable "service_type" {
  type    = string
  default = "NodePort"
}

variable "node_port" {
  type    = number
  default = null
}

variable "pvc_storage_class" {
  type    = string
  default = ""
}

variable "db_connect_url" {
  type      = string
  default   = ""
  sensitive = true
}

variable "app_version" {
  type    = string
  default = "latest"
}
