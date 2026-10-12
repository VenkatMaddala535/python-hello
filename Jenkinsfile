
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
    }
}
