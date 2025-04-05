// Define terraform provider with the specific version for consistancy
terraform {
  required_providers {
    azurerm = {
      source = "hashicorp/azurerm"
      version = "4.26.0"
    }
  }
}

provider "azurerm" {
  features {
    
  }
}

// Create a resource group
resource "azurerm_resource_group" "res_group" {
  name = "thesis-resource-group"
  location = var.location
}

// Create virtual network
resource "azurerm_virtual_network" "vnet" {
  name = "thesis-vnet"
  address_space = ["10.0.0.0/16"]
  location = azurerm_resource_group.res_group.location
  resource_group_name = azurerm_resource_group.res_group.name
}

// Create a subnet withing the virtual network
resource "azurerm_subnet" "subnet" {
    name = "thesis-subnet"
    resource_group_name = azurerm_resource_group.res_group.name
    virtual_network_name = azurerm_virtual_network.vnet.name
    address_prefixes = [ "10.0.1.0/24" ]
}

// Public IP
resource "azurerm_public_ip" "public_ip" {
    name = "thesis-public-ip"
    location = azurerm_resource_group.res_group.location
    resource_group_name = azurerm_resource_group.res_group.name
    allocation_method = "Dynamic"
}

// Network Interface for VM
resource "azurerm_network_interface" "nic" {
    name = "thesis-nic"
    location = azurerm_resource_group.res_group.location
    resource_group_name = azurerm_resource_group.res_group.name

    ip_configuration {
      name = "internal"
      subnet_id = azurerm_subnet.subnet.id
      private_ip_address_allocation = "Dynamic"
      public_ip_address_id = azurerm_public_ip.public_ip.id
    }
}

// Allow ports for Docker, app, and Prometheus
resource "azurerm_network_security_group" "nsg" {
    name = "thesis-nsg"
    location = azurerm_resource_group.res_group.location
    resource_group_name = azurerm_resource_group.res_group.name

    security_rule {
        name = "AllowHTTPApp"
        priority = 100
        direction = "Inbound"
        access = "Allow"
        protocol = "Tcp"
        source_port_range = "*"
        destination_port_range = "4000"
        source_address_prefix = "*"
        destination_address_prefix = "*"
    }

    security_rule {
        name = "AllowPrometheus"
        priority = 110
        direction = "Inbound"
        access = "Allow"
        protocol = "Tcp"
        source_port_range = "*"
        destination_port_range = "9090"
        source_address_prefix = "*"
        destination_address_prefix = "*"
    }

    security_rule {
        name = "AllowSSH"
        priority = 120
        direction = "Inbound"
        access = "Allow"
        protocol = "Tcp"
        source_port_range = "*"
        destination_port_range = "22"
        source_address_prefix = "*"
        destination_address_prefix = "*"
    }
}

resource "azurerm_network_interface_application_security_group_association" "nsg_assoc" {
    network_interface_id = azurerm_network_interface.nic.id
    application_security_group_id = azurerm_network_security_group.nsg.id
}

// Connect network security group with network interface
resource "azurerm_linux_virtual_machine" "vm" {
    name = "app-vm"
    resource_group_name = azurerm_resource_group.res_group.name
    location = azurerm_resource_group.res_group.location
    size = var.vm_size
    admin_username = var.admin_username
    network_interface_ids = [ azurerm_network_interface.nic.id, ]

    admin_ssh_key {
      username = "azureuser"
      public_key = var.public_key_path
    }

    os_disk {
      caching = "ReadWrite"
      storage_account_type = "Standard_LRS"
    }

    source_image_reference {
        publisher = "Canonical"
        offer     = "UbuntuServer"
        sku       = "18.04-LTS"
        version   = "latest"
    }

  // Provisioner to install Docker and run the app container
  custom_data = <<-EOF
              #!/bin/bash
              apt-get update
              apt-get install -y docker.io
              systemctl start docker
              docker run -d -p 4000:4000 mechykmariana/hospital-appointment-app:latest
              EOF
}