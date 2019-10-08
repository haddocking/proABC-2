pipeline {
  agent {
    docker {
      image 'continuumio/miniconda3'
    }

  }
  stages {
    stage('Install') {
      steps {
        sh 'conda clean --index-cache'
        sh 'conda env create --quiet'
      }
    }
    stage('Test') {
      steps {
        sh '''#!/bin/bash -ex
        source activate proABC-2
        conda info --envs
        export KMP_WARNINGS=noverbose
        python test_jobinput.py
        '''
      }
    }
    stage('Slack message') {
      steps {
        slackSend(channel: 'proabc_2', color: 'good', message: '*${currentBuild.currentResult}:* Job ${env.JOB_NAME} build ${env.BUILD_NUMBER}\\n More info at: ${env.BUILD_URL}')
      }
    }
  }
}