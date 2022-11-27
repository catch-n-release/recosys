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
    // try
    //     {
    //     recosysImage=docker.build("${env.ImageName}:1.0.0.${env.BUILD_ID}")

    //     recosysImage.inside()
    //         {

    //         stage("SETTING ENVIRONMENT")

    //             {

    //             // sh "pip install --upgrade pip && pip install -r /recosys/requirements.txt"
    //             sh "rm -rf reports && mkdir reports"

    //             }

    //         stage("TESTING UTILITIES")

    //             {

    //             sh "pytest -v -m utils --junitxml=reports/ml_result.xml"

    //             }

    //         stage("TESTING ML FLUX")

    //             {

    //             sh "pytest -v -m ml --junitxml=reports/ml_result.xml"

    //             }

    //         stage("TESTING APP")

    //             {

    //             sh "pytest -v -m app --junitxml=reports/app_result.xml"


    //             }

    //         stage("EXPORTING RESULTS")
    //             {

    //             sh "cp -r reports /reports"

    //             }
    //         }

    //     stage("PUBLISHING RESULTS")
    //         {
    //             junit '**/reports/*.xml'
    //             setBuildStatus("Build succeeded", "SUCCESS")
    //         }

    //     stage("PUSHING IMAGE")
    //         {

    //         withDockerRegistry([credentialsId: "dockerHub"])

    //             {

    //             recosysImage.push()

    //             }
    //         }
    //     stage("DEPLOYING APPLICATION")
    //         {

    //         def remote = [:]
    //         remote.name = "Production Server"
    //         remote.host = "128.2.205.113"
    //         remote.allowAnyHosts = true
    //         withCredentials([usernamePassword(credentialsId: 'prodServer', passwordVariable: 'password', usernameVariable: 'userName')])
    //             {
    //             remote.user = userName
    //             remote.password = password

    //             // stage("SSH Steps Rocks!") {
    //             // writeFile file: 'test.sh', text: 'ls'
    //             sshCommand remote: remote, command: "ls"
    //             // sshScript remote: remote, script: 'test.sh'
    //             // sshPut remote: remote, from: 'test.sh', into: '.'
    //             // sshGet remote: remote, from: 'test.sh', into: 'test_new.sh', override: true
    //             // sshRemove remote: remote, path: 'test.sh'
    //             // }
    //             }

    //         }
    //     }
    // catch(exc)
    //     {
    //         setBuildStatus("Build failed", "FAILURE")
    //         throw exc
    //     }
    stage("DEPLOYING APPLICATION")
            {

            def remote = [:]
            remote.name = "Production Server"
            remote.host = "128.2.205.113"
            remote.allowAnyHosts = true
            withCredentials([usernamePassword(credentialsId: 'prodServer', passwordVariable: 'password', usernameVariable: 'userName')])
                {
                remote.user = userName
                remote.password = password

                // stage("SSH Steps Rocks!") {
                // writeFile file: 'test.sh', text: 'ls'
                // sshCommand remote: remote, command: "ls"
                def commandResult = sshCommand remote: remote,
                sudo: true,
                command: "docker run -d -p 8088:80 snsrivas/recosys:1.0.0.59 uvicorn app.app:app --host 0.0.0.0 --port 80"
                echo "Result: " + commandResult
                // sshScript remote: remote, script: 'test.sh'
                // sshPut remote: remote, from: 'test.sh', into: '.'
                // sshGet remote: remote, from: 'test.sh', into: 'test_new.sh', override: true
                // sshRemove remote: remote, path: 'test.sh'
                // }
                }

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
