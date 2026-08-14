-- Depende de: setores
CREATE TABLE maquinas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    setor_id INT NOT NULL,
    tag VARCHAR(20) NOT NULL UNIQUE,
    nome VARCHAR(100) NOT NULL,
    status_vivo ENUM('Operando', 'Manutenção', 'Parado', 'Crítico') DEFAULT 'Operando',
    ultima_manutencao TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (setor_id) REFERENCES setores(id) ON DELETE RESTRICT ON UPDATE CASCADE
);
