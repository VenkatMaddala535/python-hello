
pipeline {
    agent {
        label 'pipeline-linux-agent'
    }

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


        stage('Debug workspace') {
            steps {
                sh '''
                    echo "Current workspace:"
                    pwd
                    echo "Workspace contents:"
                    ls -la
                    echo "Nested project contents:"
                    ls -la python-hello || true
                '''
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

        stage('SonarQube Analysis') {
            steps {
                dir('python-hello') {
                    withSonarQubeEnv('SonarQube') {
                        script {
                            def scannerHome = tool 'SonarScanner'
                            sh "${scannerHome}/bin/sonar-scanner"
                        }
                    }
                }
            }
        }

        stage('Build and save artifact') {
            steps {
                dir('python-hello') {
                    sh 'rm -rf dist && .venv/bin/python -m build'
                    archiveArtifacts artifacts: 'python-hello/dist/*',
                                     fingerprint: true
                }
            }
        }
    }
}

