--CREATE TABLE clientes (
--    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
--    CNPJ TEXT NOT NULL,
--    nome TEXT NOT NULL,
--    endereco TEXT NOT NULL,
--    senha TEXT NOT NULL
--);

--CREATE TABLE admins (
--    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
--    nome TEXT NOT NULL,
--    email TEXT NOT NULL,
--    senha TEXT NOT NULL
--);

--CREATE TABLE tipos_racao (
--    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
--    animal TEXT NOT NULL
--);


--CREATE TABLE racoes (
--    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
--    racao TEXT NOT NULL,
--    tipo_racao INTEGER NOT NULL,
--    estoque INTEGER NOT NULL,
--    FOREIGN KEY (tipo_racao) REFERENCES tipos_racao (id)
--);

--CREATE TABLE compras (
--    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
--    cliente TEXT NOT NULL,
 --   endereco TEXT NOT NULL,
--    data DATE NOT NULL
--);



--INSERT INTO clientes (CNPJ, nome, endereco, senha) VALUES ('00.000.000/0001-00', 'loja1', 'rua a, 111', 'aaaaa');
--INSERT INTO admins (nome, email, senha) VALUES ('adm1', 'admin@dist.com', 'scrypt:32768:8:1$ZaQ4czlWon2vav5O$669c6e15185deecf8b00ea05a27a72812c590f4c91e98ef8e49dde84d767cee7182cef9cc205f9d53b960ef9a197fee74b7be3dab10a6353441c57c71a6326e4')

--INSERT INTO tipos_racao (animal) VALUES ('cachorro');
--INSERT INTO tipos_racao (animal) VALUES ('gato');
--INSERT INTO tipos_racao (animal) VALUES ('hamster');

--INSERT INTO racoes (racao, tipo_racao, estoque) VALUES ('ração1', 1, 50);
--INSERT INTO racoes (racao, tipo_racao, estoque) VALUES ('ração2', 2, 50);
--INSERT INTO racoes (racao, tipo_racao, estoque) VALUES ('ração3', 3, 50);

UPDATE racoes SET estoque = 50 WHERE racao = 'ração1';


--SELECT * FROM racoes;

--DROP TABLE compras;