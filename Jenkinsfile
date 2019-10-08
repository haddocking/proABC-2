pipeline {
  agent {
    docker {
      image 'continuumio/miniconda3'
    }

  }
  stages {
    stage('Install') {
      steps {
        sh '''conda init bash
. ~/.bashrc
conda activate proABC-2
conda env create
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