// properties([pipelineTriggers([githubPush()])])

pipeline
    {
    /* specify nodes for executing */
        agent any
        environment
        {
            IMAGE_NAME = 'test_image'
            CONTAINER_NAME   = 'test_container'
        }

        script
        {
            def container
        }

    // def container

    stages
        {

        /* checkout repo */
        // stage('Checkout SCM')
        //     {
        //     steps
        //         {

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
                // setBuildStatus("Build Started", "PENDING")

                // ls

            //     }
            // }

        stage("Dockerizing")
        {

            steps
            {
            setBuildStatus("Build Started", "PENDING")
            script
                {
                container=docker.build("${CONTAINER_NAME}")
                // docker.image("${CONTAINER_NAME}").run()
                //     {
                //         sh ""
                //     }

                // steps{
                //     sh "docker stop ${CONTAINER_NAME} || true && docker rm ${CONTAINER_NAME} || true"
                //     sh "docker build -t ${IMAGE_NAME} --progress=plain --no-cache ."
                // }
                // conatiner.inside{
                //     sh "ls"
                //                 }
                // }
                }

            }
        }

        stage("Installing Requirements")
            {
            steps
                {

                    script
                        {
                            // docker.image("${CONTAINER_NAME}").run()
                            container.inside()
                                {
                                sh "pip install --upgrade pip && pip install -r /recosys/requirements.txt"
                                }
                        }

                // script
                //     {
                //         // container.inside
                //         //     {
                //         //     sh "pip install --upgrade pip && pip install -r /recosys/requirements.txt"
                //         //     }
                //         docker.image("${CONTAINER_NAME}").run
                //             {
                //                 sh "pip install --upgrade pip && pip install -r /recosys/requirements.txt"
                //             }
                //     }
                }


            }
        stage("Running ML Tests")
            {
            steps
                {

                    // container.inside()
                    //         {
                    //         sh "pytest -m ml"
                    //         }

                script
                    {
                        // docker.image("${CONTAINER_NAME}").run()
                        container.inside()
                        {
                            sh "pip install --upgrade pip && pip install -r /recosys/requirements.txt"
                        }
                    }
                }


            }

        stage('Do the deployment')
            {
            steps
                {
                echo ">> Run deploy applications "
                }
            }
        }

    /* Cleanup workspace */
    post
        {
    //   always {
    //       deleteDir()
    //   }
     success
        {
            setBuildStatus("Build succeeded", "SUCCESS");
        }
    failure
        {
            setBuildStatus("Build failed", "FAILURE");
        }
    }
}


void setBuildStatus(String message, String state) {
  step([
      $class: "GitHubCommitStatusSetter",
      // reposSource: [$class: "ManuallyEnteredRepositorySource", url: "https://github.com/catch-n-release/recosys.git"],
      // contextSource: [$class: "ManuallyEnteredCommitContextSource", context: "ci/jenkins/build-status"],
      // errorHandlers: [[$class: "ChangingBuildStatusErrorHandler", result: "UNSTABLE"]],
      statusResultSource: [ $class: "ConditionalStatusResultSource", results: [[$class: "AnyBuildResult", message: message, state: state]] ]
  ]);
}
