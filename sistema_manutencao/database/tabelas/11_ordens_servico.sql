-- Depende de: solicitacoes_servico, maquinas, turmas
CREATE TABLE ordens_servico (
    id INT AUTO_INCREMENT PRIMARY KEY,
    solicitacao_id INT NOT NULL,
    maquina_id INT NOT NULL,
    turma_id INT DEFAULT NULL,
    tipo_manutencao ENUM('Corretiva', 'Preventiva', 'Preditiva', 'Melhoria') NOT NULL,
    criticidade ENUM('Baixa', 'Média', 'Alta', 'Crítica') NOT NULL,
    descricao_execucao TEXT NOT NULL,
    pecas_usadas TEXT,
    data_execucao DATE NOT NULL,
    hora_inicio TIME NOT NULL,
    hora_fim TIME NOT NULL,
    quantidade_pessoas INT NOT NULL DEFAULT 1,
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (solicitacao_id) REFERENCES solicitacoes_servico(id) ON DELETE CASCADE,
    FOREIGN KEY (maquina_id) REFERENCES maquinas(id) ON DELETE CASCADE,
    FOREIGN KEY (turma_id) REFERENCES turmas(id) ON DELETE SET NULL
);
