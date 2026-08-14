CREATE DATABASE IF NOT EXISTS ctw_manutencao;
USE ctw_manutencao;

-- ====================================================================
-- 1. MÓDULO DE AUTENTICAÇÃO E RBAC (Controle de Acesso)
-- ====================================================================

CREATE TABLE perfis (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(50) NOT NULL UNIQUE,
    descricao TEXT,
    CONSTRAINT chk_perfil_nome CHECK (
        LOWER(nome) IN ('coordenador', 'gestor', 'professor', 'aluno', 'representante')
    )
);

CREATE TABLE turmas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    codigo VARCHAR(20) NOT NULL UNIQUE,
    periodo VARCHAR(20) NOT NULL
);

CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    perfil_id INT NOT NULL,
    turma_id INT DEFAULT NULL,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    senha_hash VARCHAR(255) NOT NULL,
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (perfil_id) REFERENCES perfis(id) ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (turma_id) REFERENCES turmas(id) ON DELETE SET NULL ON UPDATE CASCADE
);

CREATE TABLE logs_auditoria (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL,
    acao TEXT NOT NULL,
    endereco_ip VARCHAR(45),
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE
);

-- ====================================================================
-- 2. MÓDULO MAPA DA OFICINA E MAQUINÁRIO
-- ====================================================================

CREATE TABLE setores (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(50) NOT NULL UNIQUE,
    descricao TEXT
);

CREATE TABLE maquinas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    setor_id INT NOT NULL,
    tag VARCHAR(20) NOT NULL UNIQUE,
    nome VARCHAR(100) NOT NULL,
    status_vivo ENUM('Operando', 'Manutenção', 'Parado', 'Crítico') DEFAULT 'Operando',
    ultima_manutencao TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (setor_id) REFERENCES setores(id) ON DELETE RESTRICT ON UPDATE CASCADE
);

-- ====================================================================
-- 3. MÓDULO ALMOXARIFADO E FERRAMENTARIA
-- ====================================================================

CREATE TABLE itens_almoxarifado (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    dimensao VARCHAR(50) DEFAULT NULL,
    quantidade_atual INT NOT NULL DEFAULT 0,
    estoque_minimo INT NOT NULL DEFAULT 1,
    unidade_medida VARCHAR(10) DEFAULT 'UN',
    localizacao_gaveta VARCHAR(50)
);

CREATE TABLE alertas_estoque (
    id INT AUTO_INCREMENT PRIMARY KEY,
    item_id INT NOT NULL,
    mensagem VARCHAR(255) NOT NULL,
    status ENUM('Pendente', 'Resolvido') DEFAULT 'Pendente',
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (item_id) REFERENCES itens_almoxarifado(id) ON DELETE CASCADE
);

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

-- ====================================================================
-- 4. MÓDULO ORDENS DE SERVIÇO (O.S.) E EXECUÇÃO DE MANUTENÇÃO
-- ====================================================================

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

-- ====================================================================
-- 5. MÓDULO SOLICITAÇÃO DE COMPRAS
-- ====================================================================

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

-- ====================================================================
-- 6. MÓDULO CALENDÁRIO PREVENTIVO
-- ====================================================================

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
