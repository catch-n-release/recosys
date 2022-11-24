// properties([pipelineTriggers([githubPush()])])
// def container
node
    {
    /* specify nodes for executing */
        // agent any
        env.IMAGE_NAME = 'test_image'
        env.CONTAINER_NAME   = 'test_container'



    // def container
        setBuildStatus("Build Started", "PENDING")
        container=docker.build("${env.BUILD_ID}")
        container.inside()
            {
            try
                {

                stage("ENVIRONMENT SETUP")
                    {
                        sh "pytest ml"
                        sh "pip install --upgrade pip && pip install -r /recosys/requirements.txt"


                    }
                stage("ML FLUX TESTS")
                    {

                        sh "pytest -m ml"


                    }

                stage("APP TESTS")
                    {

                        sh "pytest -m app"
                        setBuildStatus("Build succeeded", "SUCCESS")

                    }
                }


            catch(exc)
                {
                    setBuildStatus("Build failed", "FAILURE")
                    throw
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
