pipeline {
  agent {
    docker {
      image 'continuumio/anaconda'
    }

  }
  stages {
    stage('Install') {
      steps {
        sh '''conda env create
source activate proABC-2
'''
      }
    }
    stage('Test') {
      steps {
        sh 'python -m unittest discover'
      }
    }
  }
}