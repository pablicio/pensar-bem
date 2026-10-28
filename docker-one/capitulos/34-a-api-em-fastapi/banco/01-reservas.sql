CREATE TABLE reservas (
  id        serial PRIMARY KEY,
  evento    int NOT NULL,
  assento   text NOT NULL,
  criada_em timestamptz NOT NULL DEFAULT now(),
  UNIQUE (evento, assento)
);
