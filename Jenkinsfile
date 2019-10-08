pipeline {
  agent {
    docker {
      image 'continuumio/miniconda3'
    }

  }
  stages {
    stage('Install') {
      steps {
        bash '''conda env create
conda activate proABC-2'''
      }
    }
    stage('Test') {
      steps {
        bash 'python -m unittest discover'
      }
    }
  }
}