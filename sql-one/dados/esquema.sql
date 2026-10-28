-- O esquema da Drogarias Santa Rita, como o Seu Osvaldo
-- o deixou em 2011.
CREATE TABLE lojas (
    id          integer PRIMARY KEY,
    nome        text    NOT NULL,
    cidade      text    NOT NULL,
    uf          char(2) NOT NULL,
    inaugurada  date    NOT NULL,
    metragem    integer
);

CREATE TABLE funcionarios (
    id        integer PRIMARY KEY,
    nome      text          NOT NULL,
    cargo     text          NOT NULL,
    loja_id   integer       REFERENCES lojas (id),
    chefe_id  integer       REFERENCES funcionarios (id),
    admissao  date          NOT NULL,
    salario   numeric(10,2) NOT NULL
);

CREATE TABLE categorias (
    id      integer PRIMARY KEY,
    nome    text    NOT NULL,
    pai_id  integer REFERENCES categorias (id)
);

CREATE TABLE fornecedores (
    id            integer  PRIMARY KEY,
    razao_social  text     NOT NULL,
    cnpj          char(14) NOT NULL UNIQUE,
    cidade        text     NOT NULL,
    prazo_dias    integer  NOT NULL
);

CREATE TABLE produtos (
    id             integer       PRIMARY KEY,
    nome           text          NOT NULL,
    categoria_id   integer       NOT NULL
                   REFERENCES categorias (id),
    fornecedor_id  integer       REFERENCES fornecedores (id),
    preco          numeric(10,2) NOT NULL,
    custo          numeric(10,2),
    controlado     boolean       NOT NULL,
    tarja          text,
    ativo          boolean       NOT NULL
);

CREATE TABLE lotes (
    id          integer       PRIMARY KEY,
    produto_id  integer       NOT NULL
                REFERENCES produtos (id),
    codigo      text          NOT NULL,
    fabricacao  date          NOT NULL,
    validade    date          NOT NULL,
    custo_unit  numeric(10,2) NOT NULL
);

CREATE TABLE estoque (
    loja_id     integer NOT NULL REFERENCES lojas (id),
    lote_id     integer NOT NULL REFERENCES lotes (id),
    quantidade  integer NOT NULL,
    PRIMARY KEY (loja_id, lote_id)
);

CREATE TABLE clientes (
    id            integer PRIMARY KEY,
    nome          text    NOT NULL,
    cpf           char(11),
    nascimento    date,
    cidade        text,
    fidelidade    text,
    desconto_pct  numeric(4,1)
);

CREATE TABLE vendas (
    id              integer     PRIMARY KEY,
    loja_id         integer     NOT NULL
                    REFERENCES lojas (id),
    cliente_id      integer     REFERENCES clientes (id),
    funcionario_id  integer     NOT NULL
                    REFERENCES funcionarios (id),
    momento         timestamptz NOT NULL,
    pagamento       text        NOT NULL
);

CREATE TABLE itens_venda (
    venda_id    integer       NOT NULL REFERENCES vendas (id),
    item        integer       NOT NULL,
    produto_id  integer       NOT NULL
                REFERENCES produtos (id),
    lote_id     integer       REFERENCES lotes (id),
    quantidade  integer       NOT NULL,
    preco_unit  numeric(10,2) NOT NULL,
    desconto    numeric(10,2) NOT NULL,
    PRIMARY KEY (venda_id, item)
);

CREATE TABLE receitas (
    id        integer PRIMARY KEY,
    venda_id  integer NOT NULL REFERENCES vendas (id),
    medico    text    NOT NULL,
    crm       text    NOT NULL,
    uf_crm    char(2) NOT NULL,
    emissao   date    NOT NULL
);
