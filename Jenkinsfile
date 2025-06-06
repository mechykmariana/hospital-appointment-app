pipeline{
    agent any

    environment {
        AWS_REGION = "eu-north-1"
    }

    stages {
        stage('Deploy to AWS') {
            steps {
                dir('terraform/aws') {
                withAWS(credentials: 'aws-credentials', region: "${env.AWS_REGION}") {
                    sh '''
                    terraform init
                    terraform apply -auto-approve
                    '''
                    }
                }
            }
        }

        stage('Clone Repository') {
            steps {
                git credentialsId: 'mechykmariana', url: 'https://github.com/mechykmariana/hospital-appointment-app.git', branch: 'main'
            }
        }

        stage('Check Docker Access') {
            steps {
                sh 'sudo docker ps'
            }
        }

        stage('Docker Compose Up') {
            steps {
                sh 'sudo docker-compose down || true'     // Clean up previous containers
                sh 'sudo docker-compose up -d --build'    // Build and run all containers
            }
        }
        

    //     stage('Deploy to Azure') {
    //         steps {
    //             dir('terraform/azure') {
    //             withCredentials([azureServicePrincipal(
    //                 credentialsId: 'azure-creds',
    //                 subscriptionIdVariable: 'ARM_SUBSCRIPTION_ID',
    //                 clientIdVariable: 'ARM_CLIENT_ID',
    //                 clientSecretVariable: 'ARM_CLIENT_SECRET',
    //                 tenantIdVariable: 'ARM_TENANT_ID'
    //             )]) {
    //                 sh '''
    //                 terraform init
    //                 terraform apply -auto-approve
    //                 '''
    //                 }
    //             }       
    //         }
    //     }
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
