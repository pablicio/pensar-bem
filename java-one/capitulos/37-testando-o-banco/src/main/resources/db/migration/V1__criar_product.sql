CREATE TABLE product (
    id          BIGSERIAL PRIMARY KEY,
    name        VARCHAR(120) NOT NULL,
    price       NUMERIC(10,2) NOT NULL,
    quantity    INTEGER NOT NULL DEFAULT 0,
    status      VARCHAR(20) NOT NULL,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE UNIQUE INDEX uk_product_name ON product (lower(name));
