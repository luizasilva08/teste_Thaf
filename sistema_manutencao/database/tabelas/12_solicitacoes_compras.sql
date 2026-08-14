-- Depende de: usuarios, turmas, maquinas
-- Soft delete por HERANÇA (ver notas em 03_usuarios.sql).
CREATE TABLE solicitacoes_compras (
    id_solicitacao             INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    solicitante_id             INTEGER NOT NULL REFERENCES usuarios(id_usuario) ON DELETE CASCADE,
    professor_responsavel_id   INTEGER NOT NULL REFERENCES usuarios(id_usuario) ON DELETE RESTRICT,
    turma_id                   INTEGER DEFAULT NULL REFERENCES turmas(id_turma) ON DELETE SET NULL,
    maquina_id                 INTEGER DEFAULT NULL REFERENCES maquinas(id_maquina) ON DELETE SET NULL,
    status                     status_compra_enum DEFAULT 'Não Visualizado',
    especificacao_tecnica      TEXT NOT NULL,
    quantidade_solicitacao     INTEGER NOT NULL DEFAULT 1,
    sap_solicitacao            VARCHAR(50) DEFAULT NULL,
    justificativa_solicitacao  TEXT NOT NULL,
    patrimonio                 VARCHAR(50) DEFAULT NULL,
    equipamento                VARCHAR(100) DEFAULT NULL,
    conjunto_mecanico          VARCHAR(100) DEFAULT NULL,
    arquivos                   VARCHAR(255) DEFAULT NULL,
    criado_em                  TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_solicitacoes_compras_solicitante_id  ON solicitacoes_compras (solicitante_id);
CREATE INDEX idx_solicitacoes_compras_prof_resp_id    ON solicitacoes_compras (professor_responsavel_id);
CREATE INDEX idx_solicitacoes_compras_turma_id        ON solicitacoes_compras (turma_id);
CREATE INDEX idx_solicitacoes_compras_maquina_id      ON solicitacoes_compras (maquina_id);
CREATE INDEX idx_solicitacoes_compras_status          ON solicitacoes_compras (status);

CREATE TABLE solicitacoes_compras_deletados (
    deleted_at TIMESTAMP NOT NULL DEFAULT NOW()
) INHERITS (solicitacoes_compras);

CREATE INDEX idx_solicitacoes_compras_deletados_deleted_at ON solicitacoes_compras_deletados USING BRIN (deleted_at);
CREATE INDEX idx_solicitacoes_compras_deletados_id ON solicitacoes_compras_deletados (id_solicitacao);

CREATE TRIGGER trg_soft_delete_solicitacoes_compras
    BEFORE DELETE ON solicitacoes_compras
    FOR EACH ROW EXECUTE FUNCTION fn_mover_para_historico();

CREATE VIEW vw_todos_solicitacoes_compras AS
    SELECT *, NULL::timestamp AS deleted_at FROM ONLY solicitacoes_compras
    UNION ALL
    SELECT * FROM solicitacoes_compras_deletados;
