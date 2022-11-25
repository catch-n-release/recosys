// properties([pipelineTriggers([githubPush()])])
// def container
node
    {
    /* specify nodes for executing */
        // agent any
    setBuildStatus("Build Started", "PENDING")
    env.ImageName = "snsrivas/recosys"

// def container
    recosysImage=docker.build("${env.ImageName}:latest")
        try
            {
            recosysImage.inside()
                {

                stage("SETTING ENVIRONMENT")

                    {

                    sh "pip install --upgrade pip && pip install -r /recosys/requirements.txt"
                    sh "rm -rf reports && mkdir reports"
                    }

                stage("TESTING ML FLUX")

                    {
                    sh "pwd"
                    sh "ls app/"
                    sh "pytest -v -m ml --junitxml=reports/ml_result.xml"

                    }

                stage("TESTING APP")

                    {

                    sh "pytest -v -m app --junitxml=reports/app_result.xml"


                    }

                stage("EXPORTING RESULTS")
                    {

                    sh "cp -r reports /reports"

                    }

                stage("DEPLOYING IMAGE")
                {

                withDockerRegistry([credentialsId: "dockerHub"])

                    {

                    recosysImage.push()

                    }
                }

                }

            stage("PUBLISHING RESULTS")
                {
                    junit '**/reports/*.xml'
                    setBuildStatus("Build succeeded", "SUCCESS")
                }
            }

        catch(exc)
            {
                setBuildStatus("Build failed", "FAILURE")
                throw exc
            }
    }




void setBuildStatus(String message, String state) {
  step([
      $class: "GitHubCommitStatusSetter",
      // reposSource: [$class: "ManuallyEnteredRepositorySource", url: "https://github.com/catch-n-release/recosys.git"],
      contextSource: [$class: "ManuallyEnteredCommitContextSource", context: "ci/jenkins/build-status"],
      errorHandlers: [[$class: "ChangingBuildStatusErrorHandler", result: "UNSTABLE"]],
      statusResultSource: [ $class: "ConditionalStatusResultSource", results: [[$class: "AnyBuildResult", message: message, state: state]] ]
  ]);
}
