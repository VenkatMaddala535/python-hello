pipeline {
    agent any

    stages {
        stage('Install dependencies') {
            steps {
                dir('python-hello') {
                    sh '''
                        python3.11 -m venv .venv
                        .venv/bin/python -m pip install -r requirements-dev.txt
                    '''
                }
            }
        }

        stage('Test') {
            steps {
                dir('python-hello') {
                    sh '.venv/bin/python -m pytest'
                }
            }
            post {
                always {
                    junit 'python-hello/reports/junit.xml'
                }
            }
        }

        stage('Build and save artifact') {
            steps {
                dir('python-hello') {
                    sh 'rm -rf build dist && .venv/bin/python -m build'
                    archiveArtifacts artifacts: 'dist/*', fingerprint: true
                }
            }
        }
    }
}
