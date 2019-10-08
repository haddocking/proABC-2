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
conda env create
'''
      }
    }
    stage('Test') {
      steps {
        sh '''conda activate proABC-2
python -m unittest discover'''
      }
    }
  }
}