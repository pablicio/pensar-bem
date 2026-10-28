INSERT INTO produto (nome, preco, estoque)
VALUES ('Tomate italiano', 8.90, 120);

SELECT id, nome, preco FROM produto
WHERE estoque > 0
ORDER BY nome
LIMIT 20;

UPDATE produto SET preco = 9.50 WHERE id = 1;

DELETE FROM produto WHERE id = 1;
