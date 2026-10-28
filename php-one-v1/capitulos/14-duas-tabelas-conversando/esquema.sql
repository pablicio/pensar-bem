CREATE TABLE livros (
  id      INT UNSIGNED NOT NULL AUTO_INCREMENT,
  titulo  VARCHAR(200) NOT NULL,
  autor   VARCHAR(150) NOT NULL,
  isbn    CHAR(13)     NULL,
  assunto VARCHAR(40)  NOT NULL,
  ano     SMALLINT     NULL,
  PRIMARY KEY (id),
  UNIQUE KEY uk_livros_isbn (isbn)
) ENGINE=InnoDB;

CREATE TABLE exemplares (
  id       INT UNSIGNED NOT NULL AUTO_INCREMENT,
  livro_id INT UNSIGNED NOT NULL,
  tombo    INT UNSIGNED NOT NULL,
  estado   VARCHAR(20)  NOT NULL DEFAULT 'bom',
  PRIMARY KEY (id),
  UNIQUE KEY uk_exemplares_tombo (tombo),
  FOREIGN KEY (livro_id) REFERENCES livros (id)
) ENGINE=InnoDB;

CREATE TABLE leitores (
  id          INT UNSIGNED NOT NULL AUTO_INCREMENT,
  nome        VARCHAR(120) NOT NULL,
  documento   CHAR(11)     NOT NULL,
  cadastro_em DATE         NOT NULL,
  PRIMARY KEY (id),
  UNIQUE KEY uk_leitores_documento (documento)
) ENGINE=InnoDB;

CREATE TABLE emprestimos (
  id                INT UNSIGNED NOT NULL AUTO_INCREMENT,
  exemplar_id       INT UNSIGNED NOT NULL,
  leitor_id         INT UNSIGNED NOT NULL,
  retirado_em       DATETIME     NOT NULL,
  devolver_ate      DATE         NOT NULL,
  devolvido_em      DATETIME     NULL,
  multa_em_centavos INT UNSIGNED NULL,
  PRIMARY KEY (id),
  FOREIGN KEY (exemplar_id) REFERENCES exemplares (id),
  FOREIGN KEY (leitor_id) REFERENCES leitores (id)
) ENGINE=InnoDB;
