// properties([pipelineTriggers([githubPush()])])
// def container
node
    {
    /* specify nodes for executing */
        // agent any
    cleanWs()
    checkout scm
    setBuildStatus("Build Started", "PENDING")
    env.ImageName = "snsrivas/recosys"

// def container
    try
        {
        recosysImage=docker.build("${env.ImageName}:1.0.0.${env.BUILD_ID}")

        recosysImage.inside()
            {

            stage("SETTING ENVIRONMENT")

                {

                sh "pip install --upgrade pip && pip install -r /recosys/requirements.txt"
                sh "rm -rf reports && mkdir reports"

                }

            stage("TESTING UTILITIES")

                {

                sh "pytest -v -m utils --junitxml=reports/ml_result.xml"

                }

            stage("TESTING ML FLUX")

                {

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
            }

        stage("PUBLISHING RESULTS")
            {
                junit '**/reports/*.xml'
                setBuildStatus("Build succeeded", "SUCCESS")
            }

        stage("DEPLOYING IMAGE")
            {

            withDockerRegistry([credentialsId: "dockerHub"])

                {

                recosysImage.push()

                }
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
