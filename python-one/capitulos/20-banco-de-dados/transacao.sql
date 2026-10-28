CREATE TABLE movimento (
  id          BIGSERIAL PRIMARY KEY,
  produto_id  BIGINT NOT NULL REFERENCES produto(id),
  quantidade  INTEGER NOT NULL,
  criado_em   TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

BEGIN;

UPDATE produto SET estoque = estoque - 10 WHERE id = 1;
INSERT INTO movimento (produto_id, quantidade) VALUES (1, -10);

COMMIT;
