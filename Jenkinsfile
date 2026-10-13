
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
                    sh '''
                        set -eu

                        echo "STEP 1: Checking Docker access"
                        docker info >/dev/null

                        echo "STEP 2: Checking local image"
                        docker image inspect python-hello:${BUILD_NUMBER}

                        echo "STEP 3: Logging in to Docker Hub"
                        echo "$DOCKERHUB_TOKEN" | docker login \
                            --username "$DOCKERHUB_USER" \
                            --password-stdin

                        echo "STEP 4: Tagging images"
                        docker tag python-hello:${BUILD_NUMBER} \
                            "$DOCKERHUB_REPO:${BUILD_NUMBER}"

                        docker tag python-hello:latest \
                            "$DOCKERHUB_REPO:latest"

                        echo "STEP 5: Pushing build-number tag"
                        docker push "$DOCKERHUB_REPO:${BUILD_NUMBER}"

                        echo "STEP 6: Pushing latest tag"
                        docker push "$DOCKERHUB_REPO:latest"

                        echo "STEP 7: Logging out"
                        docker logout

                        echo "Docker Hub push completed"
                    '''
                }
            }
        }
        
    }
}
