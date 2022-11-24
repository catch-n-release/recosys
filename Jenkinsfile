// properties([pipelineTriggers([githubPush()])])
// def container
node
    {
    /* specify nodes for executing */
        // agent any
        setBuildStatus("Build Started", "PENDING")
        env.IMAGE_NAME = 'test_image'
        env.CONTAINER_NAME   = 'test_container'



    // def container
        container=docker.build("${env.BUILD_ID}")
        container.inside()
            {
            try
                {

                stage("SETTING ENVIRONMENT")
                    {

                        sh "pip install --upgrade pip && pip install -r /recosys/requirements.txt"
                        sh "rm -rf reports && mkdir reports"


                    }
                stage("TESTING ML FLUX")
                    {

                        sh "pytest -v -m ml --junitxml=reports/ml_result.xml"


                    }

                stage("TESTING APP")
                    {

                        sh "pytest -v -m app --junitxml=reports/app_result.xml"
                        setBuildStatus("Build succeeded", "SUCCESS")

                    }
                stage("EXPORTING RESULTS")
                    {
                        sh "cp -r $PWD/reports /reports"
                    }
                }


            catch(exc)
                {
                    setBuildStatus("Build failed", "FAILURE")
                    throw exc
                }
            }
            stage("PUBLISHING RESULTS")
                {
                    junit '**/reports/*.xml'
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
