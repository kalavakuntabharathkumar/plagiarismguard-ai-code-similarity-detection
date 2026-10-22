pipeline {
  agent any
  stages {
    stage('Install') {
      steps {
        sh 'python -m pip install --upgrade pip'
        sh 'pip install -r requirements.txt'
      }
    }
    stage('Tests') {
      steps {
        sh 'pytest -q'
      }
    }
    stage('Build image') {
      when { branch 'main' }
      steps {
        echo 'Configure registry credentials and add docker build/push steps for your environment.'
      }
    }
  }
}
