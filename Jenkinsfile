pipeline{
    agent any

    environment {
        TF_VAR_regin = "eu-north-1"
    }

    stages {
        stage('Checkout Code') {
            steps {
                git 'https://github.com/mechykmariana/hospital-appointment-app.git'
            }
        }

        stage('Terrafrm init - AWS') {
            steps {
                // go to the directiry with the terraform code for AWS and run the init command (to initialize the backend)
                dir('terraform/aws') {
                    sh 'terraform init'
                }
            }
        }

        stage('Terrafrm plan - AWS') {
            steps {
                // go to the directiry with the terraform code for AWS and run the plan command (to plan the changes)
                dir('terraform/aws') {
                    sh 'terraform plan'
                }
            }
        }

        stage('Terrafrm apply - AWS') {
            steps {
                // go to the directiry with the terraform code for AWS and run the apply command (to apply and deploy the changes)
                dir('terraform/aws') {
                    sh 'terraform apply -auto-approve'
                }
            }
        }

        stage('Terraform Init - Azure') {
            steps {
                // go to the directiry with the terraform code for Azure and run the apply command (to apply and deploy the changes)
                dir('terraform/azure') {
                    sh 'terraform init'
                }
            }
        }

        stage('Terrafrm plan - Azure') {
            steps {
                // go to the directiry with the terraform code for Azure and run the plan command (to plan the changes)
                dir('terraform/azure') {
                    sh 'terraform plan'
                }
            }
        }

        stage('Terrafrm apply - Azure') {
            steps {
                // go to the directiry with the terraform code for Azure and run the apply command (to apply and deploy the changes)
                dir('terraform/azure') {
                    sh 'terraform apply -auto-approve'
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