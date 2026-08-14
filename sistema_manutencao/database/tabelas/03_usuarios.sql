-- Depende de: perfis, turmas
-- Soft delete por HERANÇA: DELETE move a linha para usuarios_deletados
-- (trigger fn_mover_para_historico). Consultas normais devem usar
-- "FROM ONLY usuarios" para não trazer linhas já excluídas.
CREATE TABLE usuarios (
    id_usuario     INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    perfil_id      INTEGER NOT NULL REFERENCES perfis(id_perfil) ON DELETE RESTRICT ON UPDATE CASCADE,
    turma_id       INTEGER DEFAULT NULL REFERENCES turmas(id_turma) ON DELETE SET NULL ON UPDATE CASCADE,
    nome_usuario   VARCHAR(100) NOT NULL,
    email_usuario  VARCHAR(100) NOT NULL UNIQUE,
    senha_hash     VARCHAR(255) NOT NULL,
    criado_em      TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_usuarios_perfil_id    ON usuarios (perfil_id);
CREATE INDEX idx_usuarios_turma_id     ON usuarios (turma_id);
CREATE INDEX idx_usuarios_nome_usuario ON usuarios (nome_usuario);

CREATE TABLE usuarios_deletados (
    deleted_at TIMESTAMP NOT NULL DEFAULT NOW()
) INHERITS (usuarios);

CREATE INDEX idx_usuarios_deletados_deleted_at ON usuarios_deletados USING BRIN (deleted_at);
CREATE INDEX idx_usuarios_deletados_id_usuario  ON usuarios_deletados (id_usuario);

CREATE TRIGGER trg_soft_delete_usuarios
    BEFORE DELETE ON usuarios
    FOR EACH ROW EXECUTE FUNCTION fn_mover_para_historico();

CREATE VIEW vw_todos_usuarios AS
    SELECT *, NULL::timestamp AS deleted_at FROM ONLY usuarios
    UNION ALL
    SELECT * FROM usuarios_deletados;
