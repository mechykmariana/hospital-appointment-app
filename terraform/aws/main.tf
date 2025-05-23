// Define terraform provider with the specific version for consistancy
terraform {
  required_providers {
    aws = {
      source = "hashicorp/aws"
      version = "5.94.1"
    }
  }
}

// Configure the provider and region where resourced will be deployed
provider "aws" {
    region = var.region // Stockholm region - the nearest 
}

// Create new SSH key pair for EC2 instance
resource "aws_key_pair" "thesis_key_pair" {
    key_name = var.key_name
    public_key = file("${path.module}/id_rsa.pub") // Public key file path from local machine
}

// Define a security group to allow SSH (port 22), app traffic (port 4000), and Prometheus (port 9090)
resource "aws_security_group" "allow_http" {
    name = "allow-http"
    description = "allow http and ssh traffic"

    ingress {
        from_port = 22
        to_port = 22
        protocol = "tcp"
        cidr_blocks = ["0.0.0.0/0"]
    }

    ingress {
        from_port   = 4000
        to_port     = 4000
        protocol    = "tcp"
        cidr_blocks = ["0.0.0.0/0"]
    }

    ingress {
        from_port   = 9090
        to_port     = 9090
        protocol    = "tcp"
        cidr_blocks = ["0.0.0.0/0"]
    }

    ingress {
        from_port   = 3000
        to_port     = 3000
        protocol    = "tcp"
        cidr_blocks = ["0.0.0.0/0"]
    }
    // Allow all outbound traffic (required for downloading packages, Docker image, etc.)
    egress {
        from_port   = 0
        to_port     = 0
        protocol    = "-1"
        cidr_blocks = ["0.0.0.0/0"]
  }
}

data "aws_ami" "ubuntu" {
  most_recent = true

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-*"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }

  owners = ["099720109477"] # Canonical
}

// Create ec2 instance with Docker and conainer for app automatically running inside
resource "aws_instance" "app_server" {
    ami = data.aws_ami.ubuntu.id
    instance_type = var.instance_type
    key_name = aws_key_pair.thesis_key_pair.key_name
    vpc_security_group_ids = [aws_security_group.allow_http.id]

    // Bootstrap script to run on instance startup
    user_data = <<-EOF
                #!/bin/bash
                exec > /var/log/user-data.log 2>&1
                set -x
                apt update -y
                apt install -y docker.io
                systemctl start docker
                systemctl enable docker
                sleep 10
                docker pull marianamechyk/hospital-appointment-app:latest
                docker run -d -p 4000:4000 marianamechyk/hospital-appointment-app:latest
                docker pull prom/prometheus:latest
                docker run -d -p 9090:9090 prom/prometheus:latest
                EOF


}