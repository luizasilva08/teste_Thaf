-- Depende de: itens_almoxarifado
-- Soft delete por HERANÇA (ver notas em 03_usuarios.sql).
CREATE TABLE alertas_estoque (
    id_alerta       INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    item_id         INTEGER NOT NULL REFERENCES itens_almoxarifado(id_ferramenta) ON DELETE CASCADE,
    mensagem_alerta VARCHAR(255) NOT NULL,
    status          status_alerta_enum DEFAULT 'Pendente',
    criado_em       TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_alertas_estoque_item_id ON alertas_estoque (item_id);
CREATE INDEX idx_alertas_estoque_status  ON alertas_estoque (status);

CREATE TABLE alertas_estoque_deletados (
    deleted_at TIMESTAMP NOT NULL DEFAULT NOW()
) INHERITS (alertas_estoque);

CREATE INDEX idx_alertas_estoque_deletados_deleted_at ON alertas_estoque_deletados USING BRIN (deleted_at);
CREATE INDEX idx_alertas_estoque_deletados_id ON alertas_estoque_deletados (id_alerta);

CREATE TRIGGER trg_soft_delete_alertas_estoque
    BEFORE DELETE ON alertas_estoque
    FOR EACH ROW EXECUTE FUNCTION fn_mover_para_historico();

CREATE VIEW vw_todos_alertas_estoque AS
    SELECT *, NULL::timestamp AS deleted_at FROM ONLY alertas_estoque
    UNION ALL
    SELECT * FROM alertas_estoque_deletados;
