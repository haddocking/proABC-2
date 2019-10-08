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
conda info --envs
conda activate proABC-2
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