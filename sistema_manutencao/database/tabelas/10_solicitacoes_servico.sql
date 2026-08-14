-- Depende de: maquinas, usuarios
-- Soft delete por HERANÇA (ver notas em 03_usuarios.sql).
CREATE TABLE solicitacoes_servico (
    id_ss                      INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    maquina_id                 INTEGER NOT NULL REFERENCES maquinas(id_maquina) ON DELETE CASCADE,
    solicitante_id             INTEGER NOT NULL REFERENCES usuarios(id_usuario) ON DELETE CASCADE,
    responsavel_id             INTEGER DEFAULT NULL REFERENCES usuarios(id_usuario) ON DELETE SET NULL,
    professor_validador_id     INTEGER DEFAULT NULL REFERENCES usuarios(id_usuario) ON DELETE SET NULL,
    descricao_problema         TEXT NOT NULL,
    prioridade_ss              prioridade_ss_enum DEFAULT 'Média',
    tipo_manutencao            tipo_manutencao_ss_enum DEFAULT 'Corretiva',
    status                     status_ss_enum DEFAULT 'Aberta',
    criado_em                  TIMESTAMP DEFAULT NOW(),
    atualizado_em               TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_solicitacoes_servico_maquina_id     ON solicitacoes_servico (maquina_id);
CREATE INDEX idx_solicitacoes_servico_solicitante_id ON solicitacoes_servico (solicitante_id);
CREATE INDEX idx_solicitacoes_servico_responsavel_id ON solicitacoes_servico (responsavel_id);
CREATE INDEX idx_solicitacoes_servico_prof_valid_id  ON solicitacoes_servico (professor_validador_id);
CREATE INDEX idx_solicitacoes_servico_status         ON solicitacoes_servico (status);

CREATE TABLE solicitacoes_servico_deletados (
    deleted_at TIMESTAMP NOT NULL DEFAULT NOW()
) INHERITS (solicitacoes_servico);

CREATE INDEX idx_solicitacoes_servico_deletados_deleted_at ON solicitacoes_servico_deletados USING BRIN (deleted_at);
CREATE INDEX idx_solicitacoes_servico_deletados_id ON solicitacoes_servico_deletados (id_ss);

CREATE TRIGGER trg_soft_delete_solicitacoes_servico
    BEFORE DELETE ON solicitacoes_servico
    FOR EACH ROW EXECUTE FUNCTION fn_mover_para_historico();

-- "ON UPDATE CURRENT_TIMESTAMP" do MySQL original
CREATE TRIGGER trg_touch_solicitacoes_servico
    BEFORE UPDATE ON solicitacoes_servico
    FOR EACH ROW EXECUTE FUNCTION fn_touch_atualizado_em();

CREATE VIEW vw_todos_solicitacoes_servico AS
    SELECT *, NULL::timestamp AS deleted_at FROM ONLY solicitacoes_servico
    UNION ALL
    SELECT * FROM solicitacoes_servico_deletados;
