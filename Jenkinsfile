pipeline {
    agent any

    options {
        disableConcurrentBuilds()
    }

    environment {
        IMAGE_NAME = "devsecops-demo:${BUILD_NUMBER}"
    }

    stages {
        stage('Build') {
            steps {
                sh 'docker build -t "$IMAGE_NAME" .'
            }
        }

        stage('Test') {
            steps {
                sh 'docker run --rm "$IMAGE_NAME" python -m unittest -v'
            }
        }

        stage('Deploy') {
            steps {
                sh '''
                    if docker container inspect devsecops-demo-app > /dev/null 2>&1; then
                        docker rm -f devsecops-demo-app
                    fi

                    docker run -d \
                        --name devsecops-demo-app \
                        -p 127.0.0.1:5001:5000 \
                        "$IMAGE_NAME"
                '''
            }
        }
    }
}