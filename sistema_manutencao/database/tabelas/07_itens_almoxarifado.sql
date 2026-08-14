-- Soft delete por HERANÇA (ver notas em 03_usuarios.sql).
CREATE TABLE itens_almoxarifado (
    id_ferramenta        INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nome_ferramenta      VARCHAR(100) NOT NULL,
    dimensao_ferramenta  VARCHAR(50) DEFAULT NULL,
    quantidade_atual     INTEGER NOT NULL DEFAULT 0,
    estoque_minimo       INTEGER NOT NULL DEFAULT 1,
    unidade_medida       VARCHAR(10) DEFAULT 'UN',
    localizacao_gaveta   VARCHAR(50)
);

CREATE INDEX idx_itens_almoxarifado_nome ON itens_almoxarifado (nome_ferramenta);

CREATE TABLE itens_almoxarifado_deletados (
    deleted_at TIMESTAMP NOT NULL DEFAULT NOW()
) INHERITS (itens_almoxarifado);

CREATE INDEX idx_itens_almoxarifado_deletados_deleted_at ON itens_almoxarifado_deletados USING BRIN (deleted_at);
CREATE INDEX idx_itens_almoxarifado_deletados_id ON itens_almoxarifado_deletados (id_ferramenta);

CREATE TRIGGER trg_soft_delete_itens_almoxarifado
    BEFORE DELETE ON itens_almoxarifado
    FOR EACH ROW EXECUTE FUNCTION fn_mover_para_historico();

CREATE VIEW vw_todos_itens_almoxarifado AS
    SELECT *, NULL::timestamp AS deleted_at FROM ONLY itens_almoxarifado
    UNION ALL
    SELECT * FROM itens_almoxarifado_deletados;
