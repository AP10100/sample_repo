pipeline {
    agent {
        kubernetes {
            label pipelineParams.ApplicationName+"-${labelEpochTime}-${BUILD_ID}"
            defaultContainer 'jnlp'
            yamlFile pipelineParams.JenkinsYamlPath
        }
    }

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
                sh "python3 script.py""
            }
        }
    }

}
