// properties([pipelineTriggers([githubPush()])])
// def container
setBuildStatus("Build Started", "PENDING")
node
    {
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

                stage("ENVIRONMENT SETUP")
                    {
                        // sh hello
                        sh "pip install --upgrade pip && pip install -r /recosys/requirements.txt"


                    }
                stage("ML TESTS")
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
