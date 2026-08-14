-- Soft delete IN-PLACE: DELETE vira UPDATE deleted_at (trigger fn_soft_delete_inline).
CREATE TABLE turmas (
    id_turma      INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    codigo_turma  VARCHAR(20) NOT NULL,   -- Ex: 'MAN-2026-2T'
    periodo_turma VARCHAR(20) NOT NULL,   -- Ex: 'Primeiro Turno'
    deleted_at    TIMESTAMP DEFAULT NULL
);

CREATE UNIQUE INDEX idx_turmas_codigo_ativo ON turmas (codigo_turma) WHERE deleted_at IS NULL;

CREATE TRIGGER trg_soft_delete_turmas
    BEFORE DELETE ON turmas
    FOR EACH ROW EXECUTE FUNCTION fn_soft_delete_inline('id_turma');
