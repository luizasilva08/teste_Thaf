-- Depende de: itens_almoxarifado, usuarios
-- Soft delete por HERANÇA (ver notas em 03_usuarios.sql).
CREATE TABLE registros_quebra (
    id_quebra        INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    item_id          INTEGER NOT NULL REFERENCES itens_almoxarifado(id_ferramenta) ON DELETE CASCADE,
    usuario_id       INTEGER NOT NULL REFERENCES usuarios(id_usuario) ON DELETE CASCADE,
    descricao_quebra TEXT NOT NULL,
    foto_url         VARCHAR(255),
    criado_em        TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_registros_quebra_item_id    ON registros_quebra (item_id);
CREATE INDEX idx_registros_quebra_usuario_id ON registros_quebra (usuario_id);

CREATE TABLE registros_quebra_deletados (
    deleted_at TIMESTAMP NOT NULL DEFAULT NOW()
) INHERITS (registros_quebra);

CREATE INDEX idx_registros_quebra_deletados_deleted_at ON registros_quebra_deletados USING BRIN (deleted_at);
CREATE INDEX idx_registros_quebra_deletados_id ON registros_quebra_deletados (id_quebra);

CREATE TRIGGER trg_soft_delete_registros_quebra
    BEFORE DELETE ON registros_quebra
    FOR EACH ROW EXECUTE FUNCTION fn_mover_para_historico();

CREATE VIEW vw_todos_registros_quebra AS
    SELECT *, NULL::timestamp AS deleted_at FROM ONLY registros_quebra
    UNION ALL
    SELECT * FROM registros_quebra_deletados;
