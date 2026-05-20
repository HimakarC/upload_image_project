variable "db_name" {}

variable "db_username" {}

variable "db_password" {}

variable "subnet_ids" {
  type = list(string)
}

variable "rds_name" {
  type = string
}

variable "vpc_id" {}