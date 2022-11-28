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
    env.ImageTag = "${env.ImageName}:1.0.0.${env.BUILD_ID}"

// def container
    try
        {
        recosysImage=docker.build(imageTag)

        recosysImage.inside()
            {

            stage("SETTING ENVIRONMENT")

                {

    //             // sh "pip install --upgrade pip && pip install -r /recosys/requirements.txt"
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

        stage("PUSHING IMAGE")
            {

            withDockerRegistry([credentialsId: "dockerHub"])

                {

                recosysImage.push()

                }
            }
        stage("DEPLOYING APPLICATION")
            {

            def remote = [:]
            remote.name = "Production Server"
            remote.host = "128.2.205.113"
            remote.allowAnyHosts = true
            remote.pty = true
            withCredentials([usernamePassword(credentialsId: 'prodServer', passwordVariable: 'password', usernameVariable: 'userName')])
                {
                remote.user = userName
                remote.password = password
                getDockerImage = "docker run -d -p 8089:80 ${env.ImageTag}"
                runApp = " uvicorn app.app:app --host 0.0.0.0 --port 80"
                sshCommand remote: remote, sudo:true, command: getDockerImage+runApp
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
