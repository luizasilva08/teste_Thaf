-- Depende de: setores
-- Soft delete por HERANÇA (ver notas em 03_usuarios.sql).
CREATE TABLE maquinas (
    id_maquina         INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    setor_id           INTEGER NOT NULL REFERENCES setores(id_setor) ON DELETE RESTRICT ON UPDATE CASCADE,
    tag_maquina        VARCHAR(20) NOT NULL UNIQUE,
    nome_maquina       VARCHAR(100) NOT NULL,
    status_vivo        status_maquina_enum DEFAULT 'Operando',
    ultima_manutencao  TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_maquinas_setor_id    ON maquinas (setor_id);
CREATE INDEX idx_maquinas_status_vivo ON maquinas (status_vivo);

CREATE TABLE maquinas_deletados (
    deleted_at TIMESTAMP NOT NULL DEFAULT NOW()
) INHERITS (maquinas);

CREATE INDEX idx_maquinas_deletados_deleted_at ON maquinas_deletados USING BRIN (deleted_at);
CREATE INDEX idx_maquinas_deletados_id_maquina  ON maquinas_deletados (id_maquina);

CREATE TRIGGER trg_soft_delete_maquinas
    BEFORE DELETE ON maquinas
    FOR EACH ROW EXECUTE FUNCTION fn_mover_para_historico();

-- "ON UPDATE CURRENT_TIMESTAMP" do MySQL original
CREATE TRIGGER trg_touch_maquinas
    BEFORE UPDATE ON maquinas
    FOR EACH ROW EXECUTE FUNCTION fn_touch_ultima_manutencao();

CREATE VIEW vw_todos_maquinas AS
    SELECT *, NULL::timestamp AS deleted_at FROM ONLY maquinas
    UNION ALL
    SELECT * FROM maquinas_deletados;
