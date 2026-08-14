-- Depende de: itens_almoxarifado
CREATE TABLE alertas_estoque (
    id INT AUTO_INCREMENT PRIMARY KEY,
    item_id INT NOT NULL,
    mensagem VARCHAR(255) NOT NULL,
    status ENUM('Pendente', 'Resolvido') DEFAULT 'Pendente',
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (item_id) REFERENCES itens_almoxarifado(id) ON DELETE CASCADE
);
