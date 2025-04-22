variable "namespace" {
  type    = string
  default = "feedback"
}

variable "service_type" {
  type    = string
  default = "NodePort"
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
