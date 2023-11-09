/* groovylint-disable-next-line CompileStatic */
pipeline {
            agent {
                kubernetes {
                    label pipelineParams.ApplicationName + "-${labelEpochTime}-${BUILD_ID}"

                    defaultContainer 'jnlp'
                }
            }

    stages {
        stage {
            steps {
                sh '''
                python3 script.py
                 '''
            }
        }
    }
}
