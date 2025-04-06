# Use official Jenkins image
FROM jenkins/jenkins:lts

# Switch to the root user to install all the tools
USER root

# Install required packages
RUN apt-get update && apt-get install -y \
    sudo \
    docker.io \
    unzip \
    curl \
    gnupg \
    lsb-release \
    software-properties-common \
    apt-transport-https \
    ca-certificates

# Add Docker group to Jenkins user
RUN usermod -aG docker jenkins && \
    echo "jenkins ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers

# Install AWS CLI
RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip" && \
    unzip awscliv2.zip && ./aws/install && rm -rf awscliv2.zip aws

# Install Azure CLI
RUN curl -sL https://aka.ms/InstallAzureCLIDeb | bash

# Install Terraform
ENV TERRAFORM_VERSION=1.6.6
RUN curl -fsSL https://releases.hashicorp.com/terraform/${TERRAFORM_VERSION}/terraform_${TERRAFORM_VERSION}_linux_amd64.zip -o terraform.zip && \
    unzip terraform.zip -d /usr/local/bin && \
    rm terraform.zip

USER jenkins

# Install Jenkins plugins
RUN jenkins-plugin-cli --plugins \
    aws-credentials \
    pipeline-aws \
    azure-credentials \
    docker-workflow \
    pipeline-utility-steps \
    blueocean \
    credentials-binding \
    git \
    terraform

