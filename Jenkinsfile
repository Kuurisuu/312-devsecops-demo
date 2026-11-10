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

        stage('Security Test') {
            steps {
                sh '''
                    rm -rf dependency-input reports/dependency-check
                    mkdir -p dependency-input reports/dependency-check

                    docker run --rm -i "$IMAGE_NAME" python - \
                        < export_dependencies.py \
                        > dependency-metadata.tar

                    tar -xf dependency-metadata.tar -C dependency-input
                    rm dependency-metadata.tar
                '''

                dependencyCheck(
                    odcInstallation: 'DependencyCheck',
                    nvdCredentialsId: 'nvd-api-key',
                    stopBuild: true,
                    additionalArguments: '''
                        --scan dependency-input
                        --enableExperimental
                        --format HTML
                        --format XML
                        --out reports/dependency-check
                        --data /var/jenkins_home/dependency-check-data
                    '''
                )

                dependencyCheckPublisher(
                    pattern: 'reports/dependency-check/dependency-check-report.xml'
                )
            }

            post {
                always {
                    archiveArtifacts(
                        artifacts: 'reports/dependency-check/*',
                        allowEmptyArchive: true
                    )
                }
            }
        }
    }
}