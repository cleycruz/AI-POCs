variable "project_name" {
  description = "Nombre base para los recursos"
  type        = string
  default     = "cley-logistics"
}

variable "environment" {
  description = "Ambiente de despliegue"
  type        = string
  default     = "prod"
}

variable "location" {
  description = "Región de Azure"
  type        = string
  default     = "eastus2"
}

variable "sql_admin_password" {
  description = "Password para el SQL Server"
  type        = string
  sensitive   = true # Esto evita que el password se vea en los logs de consola
}