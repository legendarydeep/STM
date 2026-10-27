// =============================================================================
// Jenkinsfile: Declarative CI Pipeline for Student Task Management System
// =============================================================================
// Prerequisites on Jenkins:
// 1. Python 3.x installed on the Jenkins agent machine (and added to system PATH)
// 2. Jenkins "JUnit Plugin" (optional but recommended to display test trends)
// =============================================================================

pipeline {
    agent any

    environment {
        PYTHONUNBUFFERED = '1'
    }

    stages {
        stage('1. Checkout Code') {
            steps {
                echo '=== Stage 1: Checking out code from version control ==='
                checkout scm
            }
        }

        stage('2. Install Dependencies') {
            steps {
                echo '=== Stage 2: Setting up dependencies from requirements.txt ==='
                // Use 'bat' for Windows agents, 'sh' for Linux/macOS agents
                script {
                    if (isUnix()) {
                        sh '''
                            python3 -m pip install --upgrade pip
                            pip install -r requirements.txt
                        '''
                    } else {
                        bat '''
                            python -m pip install --upgrade pip
                            pip install -r requirements.txt
                        '''
                    }
                }
            }
        }

        stage('3. Run Automated Tests') {
            steps {
                echo '=== Stage 3: Executing pytest test suite ==='
                // Generates standard JUnit XML report for automated test visualization
                script {
                    if (isUnix()) {
                        sh 'python3 -m pytest --junitxml=test-results.xml'
                    } else {
                        bat 'python -m pytest --junitxml=test-results.xml'
                    }
                }
            }
        }
    }

    post {
        always {
            echo '=== Archiving automated test execution results ==='
            // The JUnit plugin reads test-results.xml and renders test result graphs in Jenkins
            junit allowEmptyResults: true, testResults: 'test-results.xml'
        }
        success {
            echo '✅ Pipeline Succeeded: All tests passed. Application is healthy and ready for deployment!'
        }
        failure {
            echo '❌ Pipeline Failed: One or more unit/integration tests failed. Review test report above.'
        }
    }
}
