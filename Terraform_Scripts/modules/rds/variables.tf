variable "db_name" {}

variable "db_username" {}

variable "db_password" {}

variable "rds_name" {}

variable "subnet_ids" {
  type = list(string)
}

variable "vpc_id" {}