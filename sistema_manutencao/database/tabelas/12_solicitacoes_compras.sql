-- Depende de: usuarios, turmas, maquinas
CREATE TABLE solicitacoes_compras (
    id INT AUTO_INCREMENT PRIMARY KEY,
    solicitante_id INT NOT NULL,
    professor_responsavel_id INT NOT NULL,
    turma_id INT DEFAULT NULL,
    maquina_id INT DEFAULT NULL,
    status ENUM('Não Visualizado', 'Em Análise', 'Pedido em Andamento', 'Entregue') DEFAULT 'Não Visualizado',
    especificacao_tecnica TEXT NOT NULL,
    quantidade INT NOT NULL DEFAULT 1,
    sap VARCHAR(50) DEFAULT NULL,
    justificativa TEXT NOT NULL,
    patrimonio VARCHAR(50) DEFAULT NULL,
    equipamento VARCHAR(100) DEFAULT NULL,
    conjunto_mecanico VARCHAR(100) DEFAULT NULL,
    arquivos VARCHAR(255) DEFAULT NULL,
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (solicitante_id) REFERENCES usuarios(id) ON DELETE CASCADE,
    FOREIGN KEY (professor_responsavel_id) REFERENCES usuarios(id) ON DELETE RESTRICT,
    FOREIGN KEY (turma_id) REFERENCES turmas(id) ON DELETE SET NULL,
    FOREIGN KEY (maquina_id) REFERENCES maquinas(id) ON DELETE SET NULL
);
