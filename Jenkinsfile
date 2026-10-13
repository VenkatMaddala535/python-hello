
pipeline {
    agent { label 'pipeline-linux-agent' }

    stages {
        stage('Install dependencies') {
            steps {
                sh '''
                    python3.11 -m venv .venv
                    .venv/bin/python -m pip install -r requirements-dev.txt
                '''
            }
        }

        stage('Test') {
            steps {
                sh '.venv/bin/python -m pytest'
            }
            post {
                always {
                    junit 'reports/junit.xml'
                }
            }
        }

        stage('SonarQube Analysis') {
            steps {
                withSonarQubeEnv('SonarQube') {
                    script {
                        def scannerHome = tool 'SonarScanner'
                        sh "${scannerHome}/bin/sonar-scanner"
                    }
                }
            }
        }

        stage('Build and save artifact') {
            steps {
                sh '''
                    rm -rf dist
                    .venv/bin/python -m build
                '''
                archiveArtifacts artifacts: 'dist/*', fingerprint: true
            }
        }

        stage('Build Docker Image') {
            steps {
                sh '''
                    docker build \
                        -t python-hello:${BUILD_NUMBER} \
                        -t python-hello:latest .

                    docker images | grep python-hello
                '''
            }
        }

        stage('Push to Docker Hub') {
            steps {
                echo 'DEBUG 1: Push stage started'

                withCredentials([
                    usernamePassword(
                        credentialsId: 'dockerhub-creds',
                        usernameVariable: 'DOCKERHUB_USER',
                        passwordVariable: 'DOCKERHUB_TOKEN'
                    ),
                    string(
                        credentialsId: 'dockerhub-repo',
                        variable: 'DOCKERHUB_REPO'
                    )
                ]) {
                    echo 'DEBUG 2: Credentials bound successfully'

                    sh '''
                        set -eu

                        echo "DEBUG 3: Shell started"
                        echo "DEBUG 4: Checking Docker access"
                        docker info >/dev/null

                        echo "DEBUG 5: Checking image"
                        docker image inspect python-hello:${BUILD_NUMBER}

                        echo "DEBUG 6: Checking repository configuration"
                        test -n "$DOCKERHUB_USER"
                        test -n "$DOCKERHUB_REPO"
                        echo "Repository variable is configured"

                        echo "DEBUG 7: Logging in"
                        echo "$DOCKERHUB_TOKEN" | docker login \
                            --username "$DOCKERHUB_USER" \
                            --password-stdin

                        echo "DEBUG 8: Tagging and pushing"
                        docker tag python-hello:${BUILD_NUMBER} \
                            "$DOCKERHUB_REPO:${BUILD_NUMBER}"
                        docker push "$DOCKERHUB_REPO:${BUILD_NUMBER}"

                        docker tag python-hello:latest "$DOCKERHUB_REPO:latest"
                        docker push "$DOCKERHUB_REPO:latest"

                        docker logout
                        echo "DEBUG 9: Push completed"
                    '''
                }
            }
        }

    }
}
