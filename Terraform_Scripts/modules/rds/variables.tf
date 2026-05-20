variable "db_username" {}

variable "db_password" {}

variable "subnet_ids" {
  type = list(string)
}

variable "vpc_id" {}