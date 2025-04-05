variable "location" {
  description = "The Azure region to deploy resources in"
  type        = string
  default     = "East US"
}

variable "admin_username" {
  description = "The admin username for the VM"
  type        = string
  default     = "azureuser"
}

variable "public_key_path" {
  description = "Path to the SSH public key for the VM"
  type        = string
  default     = "~/.ssh/id_rsa.pub"
}

variable "vm_size" {
  description = "The size of the Azure VM"
  type        = string
  default     = "Standard_B1s"
}