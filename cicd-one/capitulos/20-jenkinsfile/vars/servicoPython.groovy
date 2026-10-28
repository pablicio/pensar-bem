def call(Map cfg) {
  pipeline {
    agent { label 'docker' }
    stages {
      stage('Testes') {
        steps { sh "make -C ${cfg.pasta} testes" }
      }
    }
  }
}
