// properties([pipelineTriggers([githubPush()])])

pipeline {
    /* specify nodes for executing */
    agent any
    environment {
        IMAGE_NAME = 'test_image'
        CONTAINER_NAME   = 'test_container'
    }
    def conatiner

    stages {
        /* checkout repo */
        stage('Checkout SCM') {
            steps {

                // checkout([
                //  $class: 'GitSCM',
                //  branches: [[name: 'testing']],
                //  userRemoteConfigs: [[
                //     url: 'https://github.com/catch-n-release/recosys.git',
                //     credentialsId: 'recosys0001_Wusername',
                //  ]]
                // //  updateGitlabCommitStatus: [[
                // //      name: 'build',
                // //      state: 'pending']],
                // ])
                setBuildStatus("Build Started", "PENDING")

                // ls

            }
        }

        stage("Dockerizing"){

            conatiner=docker.build("${CONTAINER_NAME}")
            // steps{
            //     sh "docker stop ${CONTAINER_NAME} || true && docker rm ${CONTAINER_NAME} || true"
            //     sh "docker build -t ${IMAGE_NAME} --progress=plain --no-cache ."
            // }
            conatiner.inside{
                sh "ls"
            }

        }

        stage("Running Container"){
            steps{

                sh "docker run -d --name ${CONTAINER_NAME} ${IMAGE_NAME}"
            }


        }

        stage('Do the deployment') {
            steps {
                echo ">> Run deploy applications "
            }
        }
    }

    /* Cleanup workspace */
    post {
    //   always {
    //       deleteDir()
    //   }
     success {
        setBuildStatus("Build succeeded", "SUCCESS");
    }
    failure {
        setBuildStatus("Build failed", "FAILURE");
    }
  }
}

void setBuildStatus(String message, String state) {
  step([
      $class: "GitHubCommitStatusSetter",
      reposSource: [$class: "ManuallyEnteredRepositorySource", url: "https://github.com/catch-n-release/recosys.git"],
      contextSource: [$class: "ManuallyEnteredCommitContextSource", context: "ci/jenkins/build-status"],
      errorHandlers: [[$class: "ChangingBuildStatusErrorHandler", result: "UNSTABLE"]],
      statusResultSource: [ $class: "ConditionalStatusResultSource", results: [[$class: "AnyBuildResult", message: message, state: state]] ]
  ]);
}
