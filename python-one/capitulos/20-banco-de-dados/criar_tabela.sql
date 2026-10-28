CREATE TABLE produto (
    id          BIGSERIAL PRIMARY KEY,
    nome        VARCHAR(120)  NOT NULL,
    preco       NUMERIC(10,2) NOT NULL CHECK (preco > 0),
    estoque     INTEGER       NOT NULL DEFAULT 0 CHECK (estoque >= 0),
    ativo       BOOLEAN       NOT NULL DEFAULT TRUE,
    criado_em   TIMESTAMPTZ   NOT NULL DEFAULT NOW()
);
