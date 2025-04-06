variable "region" {
  description = "The AWS region to deploy resources in"
  type        = string
  default     = "eu-north-1"
}

variable "key_name" {
  description = "The name of the SSH key pair"
  type        = string
  default     = "thesis-key"
}

variable "public_key_path" {
  description = "Path to the public key file"
  type        = string
  default     = "/home/marianamechyk/.ssh/id_rsa.pub"
}

variable "instance_type" {
  description = "Type of AWS EC2 instance"
  type        = string
  default     = "t3.medium"
}
