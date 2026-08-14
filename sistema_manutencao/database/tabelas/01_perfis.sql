-- Soft delete IN-PLACE: DELETE vira UPDATE deleted_at (trigger fn_soft_delete_inline).
CREATE TABLE perfis (
    id_perfil        INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nome_perfil       VARCHAR(50) NOT NULL,
    descricao_perfil TEXT,
    deleted_at        TIMESTAMP DEFAULT NULL, -- NULL = ativo
    CONSTRAINT chk_perfil_nome CHECK (LOWER(nome_perfil) IN ('coordenador','gestor','professor','aluno'))
);

-- Unicidade só entre ativos: permite reaproveitar o nome de um perfil já excluído
CREATE UNIQUE INDEX idx_perfis_nome_ativo ON perfis (nome_perfil) WHERE deleted_at IS NULL;

CREATE TRIGGER trg_soft_delete_perfis
    BEFORE DELETE ON perfis
    FOR EACH ROW EXECUTE FUNCTION fn_soft_delete_inline('id_perfil');
