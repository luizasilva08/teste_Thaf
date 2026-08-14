-- Depende de: maquinas, turmas, usuarios
CREATE TABLE calendario_preventivo (
    id INT AUTO_INCREMENT PRIMARY KEY,
    maquina_id INT NOT NULL,
    turma_id INT DEFAULT NULL,
    responsavel_id INT DEFAULT NULL,
    titulo VARCHAR(100) NOT NULL,
    descricao TEXT,
    frequencia ENUM('Diária', 'Semanal', 'Quinzenal', 'Mensal', 'Semestral', 'Anual') NOT NULL,
    data_proxima_execucao DATE NOT NULL,
    status ENUM('Agendada', 'Em Execução', 'Concluída', 'Atrasada', 'Cancelada') DEFAULT 'Agendada',
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (maquina_id) REFERENCES maquinas(id) ON DELETE CASCADE,
    FOREIGN KEY (turma_id) REFERENCES turmas(id) ON DELETE SET NULL,
    FOREIGN KEY (responsavel_id) REFERENCES usuarios(id) ON DELETE SET NULL
);
