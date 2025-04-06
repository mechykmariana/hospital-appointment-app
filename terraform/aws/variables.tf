variable "region" {
  description = "The AWS region to deploy resources in"
  type        = string
  default     = "eu-north-1"
}

variable "key_name" {
  description = "The name of the SSH key pair"
  type        = string
  default     = "id_rsa"
}

variable "public_key_path" {
  description = "Path to the public key file"
  type        = string
  default     = "/home/marianamechyk/.ssh/id_rsa.pub"
}

variable "instance_type" {
  description = "Type of AWS EC2 instance"
  type        = string
  default     = "t3.micro"
}

variable "ami_id" {
  description = "Amazon Machine Image ID for EC2 instance"
  type        = string
  default     = "ami-0274f4b62b6ae3bd5"
}
