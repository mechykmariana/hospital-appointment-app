pipeline{
    agent any

    environment {
        AWS_REGION = "eu-north-1"
    }

    stages {

        stage('Clone Repository') {
            steps {
                git credentialsId: 'your-git-credentials-id', url: 'https://github.com/mechykmariana/hospital-appointment-app.git', branch: 'main'
            }
        }

        stage('Install Terraform') {
            steps {
                sh '''
                if ! command -v terraform &> /dev/null; then
                    echo "Installing Terraform..."
                    sudo apt-get update && apt-get install -y gnupg software-properties-common curl
                    curl -fsSL https://apt.releases.hashicorp.com/gpg | gpg --dearmor -o /usr/share/keyrings/hashicorp-archive-keyring.gpg
                    echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(lsb_release -cs) main" | tee /etc/apt/sources.list.d/hashicorp.list
                    sudo apt-get update && sudo apt-get install -y terraform
                fi
                '''
            }
        }

        stage('Deploy to AWS') {
            steps {
                dir('terraform/aws') {
                withAWS(credentials: 'aws-credentials', region: "${env.AWS_REGION}") {
                    sh '''
                    cd terraform/aws
                    terraform init
                    terraform apply -auto-approve
                    '''
                    }
                }
            }
        }

        stage('Deploy to Azure') {
            steps {
                dir('terraform/azure') {
                withCredentials([azureServicePrincipal(
                    credentialsId: 'azure-creds',
                    subscriptionIdVariable: 'ARM_SUBSCRIPTION_ID',
                    clientIdVariable: 'ARM_CLIENT_ID',
                    clientSecretVariable: 'ARM_CLIENT_SECRET',
                    tenantIdVariable: 'ARM_TENANT_ID'
                )]) {
                    sh '''
                    terraform init
                    terraform apply -auto-approve
                    '''
                    }
                }       
            }
        }
    }

    post {
        success {
            echo 'Deployments successful on AWS and Azure'
        }
        failure {
            echo 'Deployment failed, check the logs for more information'
        }
    }
}