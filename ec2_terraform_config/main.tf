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

data "aws_subnet" "c16_public_subnet" {
  filter {
    name   = "tag:Name"
    values = ["c16-public-subnet-2"]
  }
}

data "aws_vpc" "c16_vpc" {
  id = "vpc-0f7ba8057a52dd82d"
}

data "aws_key_pair" "c16_josh_key_pair_week10" {
  key_name = "c16_josh_key_pair_week10"
}


resource "aws_security_group" "c16-sg-josh-allen-week10" {
  name        = "c16-sg-josh-allen-week10"
  description = "My sg for museum ec2"
  vpc_id      = data.aws_vpc.c16_vpc.id

  ingress {
    from_port        = 0
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


resource "aws_instance" "c16_josh_ec2_week10" {
  ami           = "ami-0e56583ebfdfc098f"
  instance_type = "t2.micro"
  subnet_id     = data.aws_subnet.c16_public_subnet.id
  associate_public_ip_address = true
  key_name      = data.aws_key_pair.c16_josh_key_pair_week10.key_name
  security_groups = [aws_security_group.c16-sg-josh-allen-week10.id]

  tags = {
    Name = "c16_josh_ec2_week10"
  }
}
