pipeline {
    agent any

    options {
        disableConcurrentBuilds()
    }

    environment {
        IMAGE_NAME = "devsecops-demo-322:${BUILD_NUMBER}"
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

        stage('Analyze') {
            steps {
                script {
                    def scannerHome = tool 'SonarScanner'

                    withEnv(["SCANNER_HOME=${scannerHome}"]) {
                        withSonarQubeEnv('SonarQubeLocal') {
                            withCredentials([
                                string(
                                    credentialsId: 'sonarqube-token-322',
                                    variable: 'SONAR_TOKEN'
                                )
                            ]) {
                                sh '''
                                    "$SCANNER_HOME/bin/sonar-scanner" \
                                        -Dsonar.projectKey=devsecops-demo-322 \
                                        -Dsonar.projectVersion=1.0 \
                                        -Dsonar.sources=app.py \
                                        -Dsonar.tests=test_app.py \
                                        -Dsonar.python.version=3.12 \
                                        -Dsonar.sourceEncoding=UTF-8
                                '''
                            }
                        }
                    }
                }
            }
        }
    }
}