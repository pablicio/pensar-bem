-- Os dados da Santa Rita: três lojas e as quinze
-- vendas de dezembro de 2026.

INSERT INTO categorias VALUES
    (1, 'Medicamentos', NULL),
    (2, 'Genéricos', 1),
    (3, 'Anti-hipertensivos', 2),
    (4, 'Controlados', 1),
    (5, 'Isentos de prescrição', 1),
    (6, 'Higiene e beleza', NULL),
    (7, 'Dermocosméticos', 6),
    (8, 'Infantil', NULL),
    (9, 'Fraldas', 8),
    (10, 'Serviços', NULL);

INSERT INTO fornecedores VALUES
    (1, 'Medley Ltda', '43940618000144', 'Divinópolis', 30),
    (2, 'Neoquímica Mineira Ltda', '05161069000110',
     'Itaúna', 45),
    (3, 'Dermaclin Ltda', '61092037000181', 'Belo Horizonte',
     60),
    (4, 'Kids Care Ltda', '27315948000192', 'Pará de Minas',
     30);

INSERT INTO lojas VALUES
    (1, 'Centro', 'Divinópolis', 'MG', '1978-05-02', 150),
    (2, 'Bom Pastor', 'Divinópolis', 'MG', '2006-01-26', 260),
    (3, 'Itaúna', 'Itaúna', 'MG', '2012-08-15', NULL);

INSERT INTO funcionarios VALUES
    (1, 'Cláudia Menezes', 'diretora financeira', NULL, NULL,
     '2021-06-26', 21800.00),
    (2, 'Osvaldo Ribeiro', 'analista de sistemas', NULL, 1,
     '2011-03-01', 9800.00),
    (3, 'Lúcia Amaral', 'farmacêutica RT', NULL, 1,
     '1997-09-29', 13900.00),
    (4, 'Bruna Teixeira', 'analista de dados', NULL, 2,
     '2026-12-14', 4800.00),
    (5, 'Zilda Moreira', 'gerente de loja', 1, 1,
     '2007-02-12', 7200.00),
    (6, 'Tânia Freitas', 'gerente de loja', 2, 1,
     '2005-08-10', 6900.00),
    (7, 'Marcos Rocha', 'gerente de loja', 3, 1,
     '2015-06-02', 6400.00),
    (8, 'Ana Mendes', 'farmacêutica', 1, 5, '2020-02-18',
     4950.00),
    (9, 'Bruno Dias', 'balconista', 2, 6, '2022-05-03',
     2150.00),
    (10, 'Letícia Nunes', 'caixa', 3, 7, '2023-09-11',
     1980.00);

INSERT INTO produtos VALUES
    (1, 'Losartana 50 mg 30 comp.', 3, 1, 22.27, 11.94,
     false, 'vermelha', true),
    (2, 'Dipirona 500 mg 10 comp.', 5, 2, 6.49, 2.90, false,
     NULL, true),
    (3, 'Amoxicilina 500 mg 21 cáps.', 2, 1, 24.97, 15.36,
     false, 'vermelha', true),
    (4, 'Clonazepam 2 mg 30 comp.', 4, 2, 18.90, 9.10, true,
     'preta', true),
    (5, 'Protetor solar FPS 50 120 ml', 7, 3, 68.57, 39.80,
     false, NULL, true),
    (6, 'Sérum vitamina C 30 ml', 7, 3, 129.90, NULL, false,
     NULL, true),
    (7, 'Fralda infantil M pacote 60', 9, 4, 84.23, 52.10,
     false, NULL, true),
    (8, 'Fralda geriátrica pacote 30', 9, 4, 72.40, 44.00,
     false, NULL, false),
    (9, 'Loratadina 10 mg 12 comp.', 5, 2, 14.80, 6.20,
     false, NULL, true),
    (10, 'Aferição de pressão arterial', 10, NULL, 5.00,
     NULL, false, NULL, true);

INSERT INTO lotes VALUES
    (1, 1, 'L2501031', '2025-01-10', '2027-01-10', 11.94),
    (2, 1, 'L2508114', '2025-08-20', '2027-08-20', 11.94),
    (3, 2, 'L2411207', '2024-11-05', '2026-11-30', 2.90),
    (4, 2, 'L2606032', '2026-06-01', '2028-06-01', 2.90),
    (5, 3, 'L2603088', '2026-03-10', '2027-09-10', 15.36),
    (6, 3, 'L2607015', '2026-07-02', '2028-01-02', 15.36),
    (7, 4, 'L2602440', '2026-02-14', '2028-02-14', 9.10),
    (8, 5, 'L2605301', '2026-05-20', '2028-05-20', 39.80),
    (9, 6, 'L2604122', '2026-04-01', '2027-04-01', 77.94),
    (10, 7, 'L2609050', '2026-09-05', '2029-09-05', 52.10),
    (11, 8, 'L2310020', '2023-10-02', '2025-10-02', 44.00),
    (12, 9, 'L2608077', '2026-08-07', '2028-08-07', 6.20);

INSERT INTO estoque VALUES
    (1, 1, 14),
    (1, 2, 30),
    (1, 3, 6),
    (1, 4, 40),
    (1, 5, 12),
    (1, 7, 8),
    (1, 8, 10),
    (1, 10, 20),
    (1, 12, 15),
    (2, 2, 25),
    (2, 4, 35),
    (2, 6, 18),
    (2, 7, 0),
    (2, 9, 5),
    (2, 10, 12),
    (2, 11, 3),
    (3, 1, 9),
    (3, 4, 22),
    (3, 5, 7),
    (3, 8, 4),
    (3, 12, 10);

INSERT INTO clientes VALUES
    (1, 'Maria Aparecida Souza', '34812099595', '1948-03-12',
     'Divinópolis', 'ouro', 10.0),
    (2, 'José Carlos Lima', '07145833247', '1975-07-30',
     'Divinópolis', 'prata', 5.0),
    (3, 'Juliana Rocha Alves', '16921388476', '1992-11-05',
     'Itaúna', 'bronze', 3.0),
    (4, 'Geraldo Nunes', NULL, '1939-01-20', 'Divinópolis',
     NULL, NULL),
    (5, 'Fernanda Dias Costa', '52077410639', NULL, 'Itaúna',
     NULL, NULL),
    (6, 'Paulo Henrique Martins', '86674482730',
     '1986-04-17', 'Pará de Minas', 'bronze', 3.0),
    (7, 'Raquel Teixeira', '29635107722', '2001-09-09',
     'Divinópolis', NULL, NULL),
    (8, 'Sebastião Ferreira', '74934084320', '1957-12-01',
     'Itaúna', 'prata', 5.0);

INSERT INTO vendas VALUES
    (1, 1, 1, 8, '2026-12-01 08:14:05-03:00', 'pix'),
    (2, 2, NULL, 9, '2026-12-01 10:02:44-03:00', 'dinheiro'),
    (3, 1, 4, 5, '2026-12-02 15:31:10-03:00', 'débito'),
    (4, 3, 3, 10, '2026-12-03 09:47:52-03:00', 'crédito'),
    (5, 2, 2, 9, '2026-12-04 18:20:33-03:00', 'crédito'),
    (6, 1, NULL, 8, '2026-12-07 11:05:19-03:00', 'dinheiro'),
    (7, 3, 6, 10, '2026-12-09 14:40:01-03:00', 'pix'),
    (8, 1, 1, 5, '2026-12-11 16:12:47-03:00', 'crédito'),
    (9, 2, 8, 9, '2026-12-14 09:30:00-03:00', 'pix'),
    (10, 3, NULL, 10, '2026-12-16 19:55:12-03:00', 'débito'),
    (11, 1, 7, 8, '2026-12-18 10:21:36-03:00', 'pix'),
    (12, 2, 5, 9, '2026-12-21 13:03:58-03:00', 'crédito'),
    (13, 1, 2, 5, '2026-12-23 17:48:09-03:00', 'crédito'),
    (14, 3, 3, 10, '2026-12-28 08:59:41-03:00', 'dinheiro'),
    (15, 1, NULL, 8, '2026-12-30 20:10:27-03:00', 'pix');

INSERT INTO itens_venda VALUES
    (1, 1, 1, 1, 2, 22.27, 4.45),
    (1, 2, 2, 4, 1, 6.49, 0.65),
    (2, 1, 7, 10, 1, 84.23, 0.00),
    (3, 1, 10, NULL, 1, 5.00, 0.00),
    (3, 2, 1, 2, 1, 22.27, 0.00),
    (4, 1, 3, 5, 1, 24.97, 0.75),
    (4, 2, 9, 12, 2, 14.80, 0.89),
    (5, 1, 6, 9, 1, 129.90, 6.50),
    (5, 2, 4, 7, 1, 18.90, 0.95),
    (6, 1, 2, 3, 3, 6.49, 0.00),
    (7, 1, 1, 1, 1, 22.27, 0.67),
    (7, 2, 5, 8, 1, 68.57, 2.06),
    (8, 1, 5, 8, 2, 68.57, 13.71),
    (8, 2, 9, 12, 1, 14.80, 1.48),
    (8, 3, 2, 4, 2, 6.49, 1.30),
    (9, 1, 3, 6, 1, 24.97, 1.25),
    (9, 2, 7, 10, 2, 84.23, 8.42),
    (10, 1, 10, NULL, 1, 5.00, 0.00),
    (11, 1, 3, 5, 1, 24.97, 0.00),
    (11, 2, 4, 7, 1, 18.90, 0.00),
    (12, 1, 7, 10, 1, 84.23, 0.00),
    (12, 2, 2, 4, 1, 6.49, 0.00),
    (13, 1, 5, 8, 1, 68.57, 3.43),
    (13, 2, 1, 2, 1, 22.27, 1.11),
    (13, 3, 10, NULL, 1, 5.00, 0.25),
    (14, 1, 1, 1, 2, 22.27, 1.34),
    (15, 1, 7, 10, 1, 84.23, 0.00),
    (15, 2, 2, 4, 1, 6.49, 0.00);

INSERT INTO receitas VALUES
    (1, 5, 'Dra. Helena Couto', '45213', 'MG', '2026-12-02'),
    (2, 11, 'Dr. Ricardo Paiva', '38877', 'MG', '2026-12-15');
