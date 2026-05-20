resource "aws_db_subnet_group" "subnet_group" {

  name = "${var.rds_name}-subnet-group"

  subnet_ids = var.subnet_ids
}

resource "aws_security_group" "rds_sg" {

  name = "${var.rds_name}-sg"

  vpc_id = var.vpc_id

  ingress {

    from_port = 5432
    to_port   = 5432
    protocol  = "tcp"

    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {

    from_port = 0
    to_port   = 0
    protocol  = "-1"

    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_db_instance" "postgres" {

  engine = "postgresql"

  engine_version = "16"

  instance_class = "db.t3.micro"

  allocated_storage = 20

  db_name = var.db_name

  username = var.db_username

  password = var.db_password

  publicly_accessible = true

  skip_final_snapshot = true

  db_subnet_group_name = aws_db_subnet_group.subnet_group.name

  vpc_security_group_ids = [
    aws_security_group.rds_sg.id
  ]

  tags = {
    Name = var.rds_name
  }
}
