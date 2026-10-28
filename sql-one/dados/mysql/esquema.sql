-- O esquema da Santa Rita traduzido para o MySQL 8.4.
-- As chaves estrangeiras vão no fim de cada tabela: no MySQL,
-- REFERENCES escrito ao lado da coluna é aceito e ignorado.
CREATE TABLE lojas (
    id          int          PRIMARY KEY,
    nome        varchar(60)  NOT NULL,
    cidade      varchar(60)  NOT NULL,
    uf          char(2)      NOT NULL,
    inaugurada  date         NOT NULL,
    metragem    int
);

CREATE TABLE funcionarios (
    id        int           PRIMARY KEY,
    nome      varchar(80)   NOT NULL,
    cargo     varchar(60)   NOT NULL,
    loja_id   int,
    chefe_id  int,
    admissao  date          NOT NULL,
    salario   decimal(10,2) NOT NULL,
    FOREIGN KEY (loja_id) REFERENCES lojas (id),
    FOREIGN KEY (chefe_id) REFERENCES funcionarios (id)
);

CREATE TABLE categorias (
    id      int         PRIMARY KEY,
    nome    varchar(60) NOT NULL,
    pai_id  int,
    FOREIGN KEY (pai_id) REFERENCES categorias (id)
);

CREATE TABLE fornecedores (
    id            int          PRIMARY KEY,
    razao_social  varchar(80)  NOT NULL,
    cnpj          char(14)     NOT NULL UNIQUE,
    cidade        varchar(60)  NOT NULL,
    prazo_dias    int          NOT NULL
);

CREATE TABLE produtos (
    id             int           PRIMARY KEY,
    nome           varchar(80)   NOT NULL,
    categoria_id   int           NOT NULL,
    fornecedor_id  int,
    preco          decimal(10,2) NOT NULL,
    custo          decimal(10,2),
    controlado     boolean       NOT NULL,
    tarja          varchar(20),
    ativo          boolean       NOT NULL,
    FOREIGN KEY (categoria_id) REFERENCES categorias (id),
    FOREIGN KEY (fornecedor_id) REFERENCES fornecedores (id)
);

CREATE TABLE lotes (
    id          int           PRIMARY KEY,
    produto_id  int           NOT NULL,
    codigo      varchar(20)   NOT NULL,
    fabricacao  date          NOT NULL,
    validade    date          NOT NULL,
    custo_unit  decimal(10,2) NOT NULL,
    FOREIGN KEY (produto_id) REFERENCES produtos (id)
);

CREATE TABLE estoque (
    loja_id     int NOT NULL,
    lote_id     int NOT NULL,
    quantidade  int NOT NULL,
    PRIMARY KEY (loja_id, lote_id),
    FOREIGN KEY (loja_id) REFERENCES lojas (id),
    FOREIGN KEY (lote_id) REFERENCES lotes (id)
);

CREATE TABLE clientes (
    id            int          PRIMARY KEY,
    nome          varchar(80)  NOT NULL,
    cpf           char(11),
    nascimento    date,
    cidade        varchar(60),
    fidelidade    varchar(10),
    desconto_pct  decimal(4,1)
);

CREATE TABLE vendas (
    id              int          PRIMARY KEY,
    loja_id         int          NOT NULL,
    cliente_id      int,
    funcionario_id  int          NOT NULL,
    momento         datetime     NOT NULL,
    pagamento       varchar(10)  NOT NULL,
    FOREIGN KEY (loja_id) REFERENCES lojas (id),
    FOREIGN KEY (cliente_id) REFERENCES clientes (id),
    FOREIGN KEY (funcionario_id) REFERENCES funcionarios (id)
);

CREATE TABLE itens_venda (
    venda_id    int           NOT NULL,
    item        int           NOT NULL,
    produto_id  int           NOT NULL,
    lote_id     int,
    quantidade  int           NOT NULL,
    preco_unit  decimal(10,2) NOT NULL,
    desconto    decimal(10,2) NOT NULL,
    PRIMARY KEY (venda_id, item),
    FOREIGN KEY (venda_id) REFERENCES vendas (id),
    FOREIGN KEY (produto_id) REFERENCES produtos (id),
    FOREIGN KEY (lote_id) REFERENCES lotes (id)
);

CREATE TABLE receitas (
    id        int          PRIMARY KEY,
    venda_id  int          NOT NULL,
    medico    varchar(80)  NOT NULL,
    crm       varchar(10)  NOT NULL,
    uf_crm    char(2)      NOT NULL,
    emissao   date         NOT NULL,
    FOREIGN KEY (venda_id) REFERENCES vendas (id)
);
