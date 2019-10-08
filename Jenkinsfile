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
        igblastp -germline_db_V database/IGHVp.fasta -query Example/heavy.fasta -out test
        cat test'''
      }
    }
  }
}

