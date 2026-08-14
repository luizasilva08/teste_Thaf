-- Soft delete IN-PLACE (ver notas em 01_perfis.sql).
CREATE TABLE setores (
    id_setor        INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nome_setor       VARCHAR(50) NOT NULL,
    descricao_setor TEXT,
    deleted_at       TIMESTAMP DEFAULT NULL
);

CREATE UNIQUE INDEX idx_setores_nome_ativo ON setores (nome_setor) WHERE deleted_at IS NULL;

CREATE TRIGGER trg_soft_delete_setores
    BEFORE DELETE ON setores
    FOR EACH ROW EXECUTE FUNCTION fn_soft_delete_inline('id_setor');
