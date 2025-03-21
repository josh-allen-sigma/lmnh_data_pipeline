terraform {
  required_providers {
    aws = {
      source = "hashicorp/aws"
      version = "5.89.0"
    }
  }
}

provider "aws" {
  region = "eu-west-2"
}

data "aws_vpc" "c16_vpc" {
  id = "vpc-0f7ba8057a52dd82d"
}

resource "aws_security_group" "c16-sg-josh-allen" {
  name        = "c16-sg-josh-allen"
  description = "My sg for museum db"
  vpc_id      = data.aws_vpc.c16_vpc.id

  ingress {
    from_port        = 5432
    to_port          = 5432
    protocol         = "tcp"
    cidr_blocks      = ["0.0.0.0/0"]
    ipv6_cidr_blocks = ["::/0"]
  }

  egress {
    from_port        = 0
    to_port          = 0
    protocol         = -1
    cidr_blocks      = ["0.0.0.0/0"]
    ipv6_cidr_blocks = ["::/0"]
  }
  tags = {
    Name = "c16-sg-josh-allen"
  }
}


resource "aws_db_instance" "c16-josh-museum-rds" {
  allocated_storage            = 10
  db_name                      = "joshallenmuseum"
  identifier                   = "c16-josh-museum-rds"
  engine                       = "postgres"
  engine_version               = "17.4"
  instance_class               = "db.t3.micro"
  publicly_accessible          = true
  performance_insights_enabled = false
  skip_final_snapshot          = true
  db_subnet_group_name         = "c16-public-subnet-group"
  vpc_security_group_ids       = [aws_security_group.c16-sg-josh-allen.id]
  username                     = var.DB_USERNAME
  password                     = var.DB_PASSWORD
}