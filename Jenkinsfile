pipeline {
    agent any
    stages {
        stage('Build') {
            when {
                branch 'dev'
            }
            steps {
                echo "====== BUILD STAGE ======"
                sh '''
                    virtualenv venv -p python3.8
                    . venv/bin/activate
                    venv/bin/pip install --no-deps -r requirements.txt
                '''
            }
        }
    }
}