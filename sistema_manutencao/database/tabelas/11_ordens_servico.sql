-- Depende de: solicitacoes_servico, maquinas, turmas
-- Soft delete por HERANÇA (ver notas em 03_usuarios.sql).
CREATE TABLE ordens_servico (
    id_os                INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    solicitacao_id       INTEGER NOT NULL REFERENCES solicitacoes_servico(id_ss) ON DELETE CASCADE,
    maquina_id           INTEGER NOT NULL REFERENCES maquinas(id_maquina) ON DELETE CASCADE,
    turma_id             INTEGER DEFAULT NULL REFERENCES turmas(id_turma) ON DELETE SET NULL,
    tipo_manutencao      tipo_manutencao_os_enum NOT NULL,
    criticidade_os       criticidade_os_enum NOT NULL,
    descricao_execucao   TEXT NOT NULL,
    pecas_usadas         TEXT,
    data_execucao        DATE NOT NULL,
    hora_inicio          TIME NOT NULL,
    hora_fim              TIME NOT NULL,
    quantidade_pessoas   INTEGER NOT NULL DEFAULT 1,
    criado_em            TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_ordens_servico_solicitacao_id ON ordens_servico (solicitacao_id);
CREATE INDEX idx_ordens_servico_maquina_id     ON ordens_servico (maquina_id);
CREATE INDEX idx_ordens_servico_turma_id       ON ordens_servico (turma_id);
CREATE INDEX idx_ordens_servico_data_execucao  ON ordens_servico (data_execucao);

CREATE TABLE ordens_servico_deletados (
    deleted_at TIMESTAMP NOT NULL DEFAULT NOW()
) INHERITS (ordens_servico);

CREATE INDEX idx_ordens_servico_deletados_deleted_at ON ordens_servico_deletados USING BRIN (deleted_at);
CREATE INDEX idx_ordens_servico_deletados_id ON ordens_servico_deletados (id_os);

CREATE TRIGGER trg_soft_delete_ordens_servico
    BEFORE DELETE ON ordens_servico
    FOR EACH ROW EXECUTE FUNCTION fn_mover_para_historico();

CREATE VIEW vw_todos_ordens_servico AS
    SELECT *, NULL::timestamp AS deleted_at FROM ONLY ordens_servico
    UNION ALL
    SELECT * FROM ordens_servico_deletados;
