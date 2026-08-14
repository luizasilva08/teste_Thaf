-- Depende de: maquinas, usuarios
CREATE TABLE solicitacoes_servico (
    id INT AUTO_INCREMENT PRIMARY KEY,
    maquina_id INT NOT NULL,
    solicitante_id INT NOT NULL,
    responsavel_id INT DEFAULT NULL,
    professor_validador_id INT DEFAULT NULL,
    descricao_problema TEXT NOT NULL,
    prioridade_ss ENUM('Baixa', 'Média', 'Alta') DEFAULT 'Média',
    tipo_manutencao ENUM('Corretiva', 'Preventiva', 'Preditiva') DEFAULT 'Corretiva',
    status ENUM('Aberta', 'Em Análise', 'Aguardando Peças', 'Execução', 'Validação', 'Concluída') DEFAULT 'Aberta',
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    atualizado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (maquina_id) REFERENCES maquinas(id) ON DELETE CASCADE,
    FOREIGN KEY (solicitante_id) REFERENCES usuarios(id) ON DELETE CASCADE,
    FOREIGN KEY (responsavel_id) REFERENCES usuarios(id) ON DELETE SET NULL,
    FOREIGN KEY (professor_validador_id) REFERENCES usuarios(id) ON DELETE SET NULL
);
