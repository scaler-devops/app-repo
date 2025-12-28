pipeline {
    agent any

    environment {
        IMAGE_NAME = "rashmikakashyap/gitops-demo-app"
        IMAGE_TAG  = "${GIT_COMMIT.substring(0,7)}"
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                sh '''
                docker build -t ${IMAGE_NAME}:${IMAGE_TAG} .
                '''
            }
        }

        stage('Push Docker Image') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-creds',
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS'
                )]) {
                    sh '''
                    echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin
                    docker push ${IMAGE_NAME}:${IMAGE_TAG}
                    '''
                }
            }
        }

        stage('Update Kubernetes Manifests') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'github-creds',
                    usernameVariable: 'GIT_USER',
                    passwordVariable: 'GIT_TOKEN'
                )]) {
                    sh '''
                    git checkout main

                    git pull --rebase https://${GIT_USER}:${GIT_TOKEN}@github.com/scaler-devops/app-repo.git main

                    sed -i "s|image: .*|image: ${IMAGE_NAME}:${IMAGE_TAG}|" manifests/deployment.yaml

                    git config user.email "ci@example.com"
                    git config user.name "Jenkins CI"

                    git add manifests/deployment.yaml
                    git commit -m "ci: update image to ${IMAGE_TAG}" || true

                    git push https://${GIT_USER}:${GIT_TOKEN}@github.com/scaler-devops/app-repo.git main
                    '''
                }
            }
        }
    }
}
