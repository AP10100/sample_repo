pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                // Checkout the code from the GitHub repository
                script {
                    checkout scm
                }
            }
        }

        stage('Run Python Script') {
            steps {
                // Assuming your Python script is named 'your_script.py'
                sh "python3 demo.py"
            }
        }
    }

}
