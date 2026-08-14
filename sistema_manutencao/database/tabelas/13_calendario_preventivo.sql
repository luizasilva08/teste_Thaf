-- Depende de: maquinas, turmas, usuarios
-- Soft delete por HERANÇA (ver notas em 03_usuarios.sql).
CREATE TABLE calendario_preventivo (
    id_calendario           INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    maquina_id              INTEGER NOT NULL REFERENCES maquinas(id_maquina) ON DELETE CASCADE,
    turma_id                INTEGER DEFAULT NULL REFERENCES turmas(id_turma) ON DELETE SET NULL,
    responsavel_id          INTEGER DEFAULT NULL REFERENCES usuarios(id_usuario) ON DELETE SET NULL,
    titulo_calendario       VARCHAR(100) NOT NULL,
    descricao_calendario    TEXT,
    frequencia_calendario   frequencia_cal_enum NOT NULL,
    data_proxima_execucao   DATE NOT NULL,
    status                  status_cal_enum DEFAULT 'Agendada',
    criado_em               TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_calendario_preventivo_maquina_id     ON calendario_preventivo (maquina_id);
CREATE INDEX idx_calendario_preventivo_turma_id       ON calendario_preventivo (turma_id);
CREATE INDEX idx_calendario_preventivo_responsavel_id ON calendario_preventivo (responsavel_id);
CREATE INDEX idx_calendario_preventivo_status         ON calendario_preventivo (status);
CREATE INDEX idx_calendario_preventivo_data_prox_exec ON calendario_preventivo (data_proxima_execucao);

CREATE TABLE calendario_preventivo_deletados (
    deleted_at TIMESTAMP NOT NULL DEFAULT NOW()
) INHERITS (calendario_preventivo);

CREATE INDEX idx_calendario_preventivo_deletados_deleted_at ON calendario_preventivo_deletados USING BRIN (deleted_at);
CREATE INDEX idx_calendario_preventivo_deletados_id ON calendario_preventivo_deletados (id_calendario);

CREATE TRIGGER trg_soft_delete_calendario_preventivo
    BEFORE DELETE ON calendario_preventivo
    FOR EACH ROW EXECUTE FUNCTION fn_mover_para_historico();

CREATE VIEW vw_todos_calendario_preventivo AS
    SELECT *, NULL::timestamp AS deleted_at FROM ONLY calendario_preventivo
    UNION ALL
    SELECT * FROM calendario_preventivo_deletados;
