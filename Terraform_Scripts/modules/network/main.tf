# =========================================
# DEFAULT VPC
# =========================================

data "aws_vpc" "default" {

  default = true
}

# =========================================
# DEFAULT SUBNETS
# =========================================

data "aws_subnets" "default" {

  filter {

    name = "vpc-id"

    values = [data.aws_vpc.default.id]
  }
}