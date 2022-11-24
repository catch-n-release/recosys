// properties([pipelineTriggers([githubPush()])])
// def container
node
    {
        setBuildStatus("Build Started", "PENDING")
    /* specify nodes for executing */
        // agent any
        env.IMAGE_NAME = 'test_image'
        env.CONTAINER_NAME   = 'test_container'



    // def container
        container=docker.build("${env.BUILD_ID}")
        container.inside()
            {
            try
                {

                stage("Installing Requirements")
                    {

                        sh "pip install --upgrade pip && pip install -r /recosys/requirements.txt"


                    }
                stage("Running ML Tests")
                    {

                        sh "pytest -m ml"

                        setBuildStatus("Build succeeded", "SUCCESS")

                    }

                stage('Do the deployment')
                    {

                        echo ">> Run deploy applications "

                    }
                }


            catch(exc)
                {
                    setBuildStatus("Build failed", "FAILURE")
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
