pipeline {
  agent {
    docker {
      image 'continuumio/miniconda3'
    }

  }
  stages {
    stage('Install') {
      steps {
        sh '''
        conda init bash
        bash /opt/conda/etc/profile.d/conda.csh
        bash /root/.bashrc
        conda env create
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
