-- Depende de: usuarios
-- Soft delete por HERANÇA (ver notas em 03_usuarios.sql).
CREATE TABLE logs_auditoria (
    id          INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    usuario_id  INTEGER NOT NULL REFERENCES usuarios(id_usuario) ON DELETE CASCADE,
    acao        TEXT NOT NULL,
    endereco_ip VARCHAR(45),
    criado_em   TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_logs_auditoria_usuario_id ON logs_auditoria (usuario_id);
CREATE INDEX idx_logs_auditoria_criado_em  ON logs_auditoria (criado_em);

CREATE TABLE logs_auditoria_deletados (
    deleted_at TIMESTAMP NOT NULL DEFAULT NOW()
) INHERITS (logs_auditoria);

CREATE INDEX idx_logs_auditoria_deletados_deleted_at ON logs_auditoria_deletados USING BRIN (deleted_at);
CREATE INDEX idx_logs_auditoria_deletados_id ON logs_auditoria_deletados (id);

CREATE TRIGGER trg_soft_delete_logs_auditoria
    BEFORE DELETE ON logs_auditoria
    FOR EACH ROW EXECUTE FUNCTION fn_mover_para_historico();

CREATE VIEW vw_todos_logs_auditoria AS
    SELECT *, NULL::timestamp AS deleted_at FROM ONLY logs_auditoria
    UNION ALL
    SELECT * FROM logs_auditoria_deletados;
