pipeline {
    agent any

    environment {
        DOCKER_IMAGE  = "neeraj91/flask-app"
        DOCKER_TAG    = "${BUILD_NUMBER}"
    }

    stages {

        stage('Build Docker Image') {
            steps {
                sh "docker build -t ${DOCKER_IMAGE}:${DOCKER_TAG} ."
            }
        }

        stage('Push to DockerHub') {
            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: 'dockerhub-credentials',
                        usernameVariable: 'Dockername',
                        passwordVariable: 'Dockervars'
                    )
                ]) {
                    sh '''
                        echo "$Dockervars" | docker login -u "$Dockername" --password-stdin

                        docker push $DOCKER_IMAGE:$DOCKER_TAG

                        docker tag $DOCKER_IMAGE:$DOCKER_TAG $DOCKER_IMAGE:latest

                        docker push $DOCKER_IMAGE:latest
                    '''
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                withCredentials([aws(accessKeyVariable: 'AWS_ACCESS_KEY_ID', credentialsId: 'aws-creds', secretKeyVariable: 'AWS_SECRET_ACCESS_KEY')])
                {
                sh '''
                
                aws eks update-kubeconfig --name test-cluster --region ap-southeast-1
                envsubst < deployment.yaml | kubectl apply -f - 
                kubectl rollout status deployment myapp --timeout=5m

                '''
                }
            } 

            post {

                success {

                    echo "Deployment succeeded - myapp is healty and roll out"
                    kubectl set image deployment myapp myapp=neeraj91/prometheus-app:nonexistent
                }

                failure {

                    echo "Deployment failed - myapp is failing on deployment"
                    withCredentials([aws(accessKeyVariable: 'AWS_ACCESS_KEY_ID', credentialsId: 'aws-creds', secretKeyVariable: 'AWS_SECRET_ACCESS_KEY')])
                    { 
                        
                    sh '''

                    aws eks update-kubeconfig --name test-cluster --region ap-southeast-1
                    kubectl rollout undo deployment myapp
                    kubectl rollout status deployment myapp --timeout-5m

                    '''
                    }
                }
            }
        }
    }

    post
    {
        always {
            cleanWs()
        }
    }
}
