pipeline {
  agent any
  parameters {
    string(name: 'TAG',
    description: 'Tag  for production server')
    string(name: 'HOSTS',
    defaultValue: 'hostvirtual2',
    description: 'Hosts Parameters for production server')
  }
  stages {
    stage('hm_sonar') {
        environment {
          SONAR_SCANNER_OPTS = "-Xmx1g"
        }
      steps {
        sh "pwd"
        sh "/opt/sonar-scanner/bin/sonar-scanner -D sonar-project.properties"
      }
    }
    stage('hm_build') {
      steps {
        echo 'Here is a step Build named Hm_Build '
        checkout([$class: 'GitSCM', branches: [[name: '*/develop']], doGenerateSubmoduleConfigurations: false, extensions: [], submoduleCfg: [], userRemoteConfigs: [[url: '']]])
        sh './projects/hm/hm_build.sh'
        slackSend baseUrl: '', channel: 'health_monitor', color: 'Green', message: 'Health Monitor Build Successfully', token: 'CiNUGrFdmnNqGSNFz80YJjL3'
      }
    }
    stage('hm_deply') {
      steps {
        echo 'Deploying project on staging server'
        checkout([$class: 'GitSCM', branches: [[name: '*/develop']], doGenerateSubmoduleConfigurations: false, extensions: [], submoduleCfg: [], userRemoteConfigs: [[url: '']]])
        sh './projects/hm/hm_deploy.sh'
        slackSend baseUrl: 'URL', channel: 'health_monitor', color: 'Green', message: 'HEalth Monitor Deployed Successfully', token: ''
      }
    }
    stage('hm_prod') {
      steps {
        echo 'Installing project on production server'
        checkout([$class: 'GitSCM', branches: [[name: '*/master']], doGenerateSubmoduleConfigurations: false, extensions: [], submoduleCfg: [], userRemoteConfigs: [[url: '']]])
        sh './projects/hm/hm_prod.sh $TAG $HOSTS'
        slackSend baseUrl: 'URL', channel: 'health_monitor', color: 'Red', message: 'Deploying Production server', token: ''
      }
    }
  }
}

