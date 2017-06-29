// https://jenkins.io/doc/pipeline/tour/running-multiple-steps/
// https://jenkins.io/doc/pipeline/tour/post/
// https://jenkins.io/doc/pipeline/tour/deployment/

pipeline {
    agent any
    stages {
        stage('build') {
            steps {
                bat 'hello.bat'
                bat 'python hello.py'
            }
        }
        stage('Test') {
            steps {
                echo 'Testing'
            }
        }
        stage("Deploy") {
            steps {
                echo "Deploying"
            }
        }
    }
    post {
        always {
            echo 'This will always run'
            // TODO: Review build log from build 11
            // mail to: 'stuarthoye@gmail.com',
            //    subject: "Notification about ${currentBuild.fullDisplayName}",
            //    body: "URL:  ${env.BUILD_URL}"
        }
        success {
            echo 'This will run only if successful'
        }
        failure {
            echo 'This will run only if failed'
        }
        unstable {
            echo 'This will run only if the run was marked as unstable'
        }
        changed {
            echo 'This will run only if the state of the Pipeline has changed'
            echo 'For example, if the Pipeline was previously failing but is now successful'
        }
    }
}