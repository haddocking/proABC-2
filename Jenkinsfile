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
         sh '''conda env create'''
      }
    }
    stage('Test') {
      steps {
        sh '''#!/bin/bash -ex
        conda info --envs
        source activate proABC-2
        python test_jobinput.py'''
      }
    }
  }
}