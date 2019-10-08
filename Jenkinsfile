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
         sh '''conda env create --quiet'''
      }
    }
    stage('Test') {
      steps {
        sh '''#!/bin/bash -ex
        source activate proABC-2
        conda info --envs
        export KMP_WARNINGS=noverbose
        python proABC.py Example heavy.fasta light.fasta
        '''
      }
    }
  }
}

