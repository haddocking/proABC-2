def COLOR_MAP = ['SUCCESS': 'good', 'FAILURE': 'danger', 'UNSTABLE': 'danger', 'ABORTED': 'danger']

pipeline {
  agent {
    docker {
      image 'continuumio/miniconda3'
    }

  }
  stages {

    try {
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
        export KMP_WARNINGS=noverbose
        python -m coverage run -m unittest discover
        export CODECOV_TOKEN=686a06a1-4987-462a-bad5-650f80db5866
        codecov
        '''
      }
    }
    } catch (e) {
    throw e
    } finally {
    stage('Slack message') {
      steps {
        slackSend(channel: 'proabc_2',
        color: COLOR_MAP[currentBuild.currentResult],
        message: "*${currentBuild.currentResult}:* Job ${env.JOB_NAME} build ${env.BUILD_NUMBER}\nMore info at: ${env.BUILD_URL}")
        }
      }
    }
  }
}