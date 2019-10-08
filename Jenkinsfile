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
        export -f conda
        export -f __conda_activate
        export -f __conda_reactivate
        export -f __conda_hashr
        export -f __add_sys_prefix_to_path
        eval "$(conda shell.bash hook)
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
