-- Depende de: itens_almoxarifado, usuarios
CREATE TABLE registros_quebra (
    id INT AUTO_INCREMENT PRIMARY KEY,
    item_id INT NOT NULL,
    usuario_id INT NOT NULL,
    descricao TEXT NOT NULL,
    foto_url VARCHAR(255),
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (item_id) REFERENCES itens_almoxarifado(id) ON DELETE CASCADE,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE
);
