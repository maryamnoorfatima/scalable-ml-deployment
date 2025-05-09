pipeline {
    agent any
    
    environment {
        DOCKER_HUB_REPO = 'your-dockerhub-username/innovate-analytics-mlops'
        DOCKER_HUB_CRED = 'dockerhub-credentials'
    }
    
    stages {
        stage('Build') {
            steps {
                sh 'docker build -t $DOCKER_HUB_REPO:$BUILD_NUMBER .'
            }
        }
        
        stage('Test') {
            steps {
                sh 'docker run $DOCKER_HUB_REPO:$BUILD_NUMBER python -m pytest tests/'
            }
        }
        
        stage('Push') {
            steps {
                withCredentials([usernamePassword(credentialsId: DOCKER_HUB_CRED, usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    sh '''
                        echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin
                        docker push $DOCKER_HUB_REPO:$BUILD_NUMBER
                    '''
                }
            }
        }
    }
} 