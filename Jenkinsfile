pipeline {
  agent {
    docker {
      image 'python:3.6'
    }

  }
  stages {
    stage('Install') {
      steps {
        sh '''
        wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh -O miniconda.sh
        bash miniconda.sh -b -p $HOME/miniconda
        export PATH="$HOME/miniconda/bin:$PATH"
        hash -r
        conda config --set always_yes yes --set changeps1 no
        conda update -q conda
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
