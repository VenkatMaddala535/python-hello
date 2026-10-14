
pipeline {
    agent { label 'pipeline-agent' }

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
                    )
                ]) {
                    sh '''
                        set -eu

                        echo "DEBUG 2: Credentials loaded"
                        DOCKERHUB_REPO="${DOCKERHUB_USER}/python-hello"

                        echo "DEBUG 3: Checking Docker access"
                        docker info >/dev/null

                        echo "DEBUG 4: Logging in"
                        # docker login --username <username> --password-stdin
                        echo "$DOCKERHUB_TOKEN" | docker login --username "$DOCKERHUB_USER" --password-stdin

                        echo "DEBUG 5: Tagging images"
                        # docker tag SOURCE_IMAGE[:TAG] TARGET_IMAGE[:TAG]
                        docker tag python-hello:${BUILD_NUMBER} "$DOCKERHUB_REPO:${BUILD_NUMBER}"
                        docker tag python-hello:latest "$DOCKERHUB_REPO:latest"

                        echo "DEBUG 6: Pushing images"
                        docker push "$DOCKERHUB_REPO:${BUILD_NUMBER}"
                        docker push "$DOCKERHUB_REPO:latest"

                        docker logout
                        echo "DEBUG 7: Push completed"
                    '''
                }
            }
        }

    }
}
