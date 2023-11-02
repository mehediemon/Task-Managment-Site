pipeline {
    agent any
    stages {
        stage('Build') {
            when {
                branch 'dev'
            }
            steps { 
                echo 'Hello World dev'
            }
        }
    }
}