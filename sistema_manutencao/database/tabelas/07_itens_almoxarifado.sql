CREATE TABLE itens_almoxarifado (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    dimensao VARCHAR(50) DEFAULT NULL,
    quantidade_atual INT NOT NULL DEFAULT 0,
    estoque_minimo INT NOT NULL DEFAULT 1,
    unidade_medida VARCHAR(10) DEFAULT 'UN',
    localizacao_gaveta VARCHAR(50)
);
