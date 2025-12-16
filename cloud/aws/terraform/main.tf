# main.tf


## Run with:
## terraform init
## terraform apply -auto-approve \
##   -var set_name=cfd-run-01 \
##   -var public_key="$(cat ~/.ssh/cfd-key.pub)" \
##   -var instance_count=3


terraform {
  required_providers {
    aws = { source = "hashicorp/aws", version = "~> 5.0" }
  }
}

provider "aws" {
  region = var.region
}

# VPC + subnet + routing for public IPs
resource "aws_vpc" "rg" {
  cidr_block           = var.vpc_cidr
  enable_dns_support   = true
  enable_dns_hostnames = true
  tags = { Name = "${var.set_name}-vpc", Project = var.set_name }
}

resource "aws_internet_gateway" "igw" {
  vpc_id = aws_vpc.rg.id
  tags   = { Name = "${var.set_name}-igw", Project = var.set_name }
}

resource "aws_subnet" "public" {
  vpc_id                  = aws_vpc.rg.id
  cidr_block              = var.subnet_cidr
  map_public_ip_on_launch = true
  tags = { Name = "${var.set_name}-subnet", Project = var.set_name }
}

resource "aws_route_table" "public" {
  vpc_id = aws_vpc.rg.id
  route { cidr_block = "0.0.0.0/0"; gateway_id = aws_internet_gateway.igw.id }
  tags = { Name = "${var.set_name}-rt", Project = var.set_name }
}

resource "aws_route_table_association" "public" {
  subnet_id      = aws_subnet.public.id
  route_table_id = aws_route_table.public.id
}

# Security group (per VPC)
resource "aws_security_group" "svc" {
  name        = "${var.set_name}-sg"
  description = "CFD service SG"
  vpc_id      = aws_vpc.rg.id
  ingress { protocol = "tcp" from_port = 22   to_port = 22   cidr_blocks = [var.ssh_cidr] }
  ingress { protocol = "tcp" from_port = 4444 to_port = 4444 cidr_blocks = var.app_cidrs }
  ingress { protocol = "tcp" from_port = 4445 to_port = 4445 cidr_blocks = var.app_cidrs }
  egress  { protocol = "-1" from_port = 0     to_port = 0    cidr_blocks = ["0.0.0.0/0"] }
  tags = { Name = "${var.set_name}-sg", Project = var.set_name }
}

# Key pair (optional: reuse existing by name)
resource "aws_key_pair" "kp" {
  key_name   = var.key_name
  public_key = var.public_key
}

# Instances (1..4)
data "aws_ssm_parameter" "al2023" {
  name = "/aws/service/ami-amazon-linux-latest/al2023-ami-kernel-6.1-x86_64"
}
resource "aws_instance" "node" {
  ami                    = data.aws_ssm_parameter.al2023.value
  instance_type          = var.instance_type
  count                  = var.instance_count
  subnet_id              = aws_subnet.public.id
  vpc_security_group_ids = [aws_security_group.svc.id]
  key_name               = aws_key_pair.kp.key_name
  associate_public_ip_address = true

  root_block_device {
    volume_type = "gp3"
    volume_size = var.instance_disk_size
    delete_on_termination = true
  }

  ##  ebs_block_device {
  ##    device_name = "/dev/xvdf"
  ##    volume_type = "gp3"
  ##    volume_size = var.instance_disk_size
  ##    delete_on_termination = true
  ##  }

  user_data = file(var.user_data_file)

  user_data = templatefile("${path.module}/userdata.sh.tmpl", {
    ec2user                  = var.ec2user
    docker_registry_url      = var.docker_registry_url
    docker_registry_username = var.docker_registry_username
    docker_registry_password = var.docker_registry_password
    cfd_image                = var.cfd_image
  })

  tags = { Name = "${var.set_name}-node-${count.index}", Project = var.set_name }
}

output "public_ips" {
  value = [for i in aws_instance.node : i.public_ip]
}

