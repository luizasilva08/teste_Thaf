-- Funções de suporte ao soft delete. Compartilhado entre várias tabelas —
-- não são donas de nenhuma classe específica, só mexa aqui se for criar uma
-- função de suporte nova (ex: outro "fn_touch_*").

-- Move a linha excluída para "<tabela>_deletados" e deixa o DELETE concluir
-- na tabela principal. Usada pelas tabelas do padrão "herança".
CREATE OR REPLACE FUNCTION fn_mover_para_historico()
RETURNS TRIGGER AS $$
BEGIN
    EXECUTE format('INSERT INTO %I SELECT ($1).*, now()', TG_TABLE_NAME || '_deletados')
    USING OLD;
    RETURN OLD; -- permite que o DELETE original prossiga na tabela principal
END;
$$ LANGUAGE plpgsql;

-- Converte um DELETE em UPDATE (deleted_at = now()) e cancela a remoção
-- física. Genérica para qualquer PK: o nome da coluna de PK é passado como
-- argumento do trigger (TG_ARGV[0]), já que cada tabela usa um nome
-- diferente (id_perfil, id_setor, id_turma...).
CREATE OR REPLACE FUNCTION fn_soft_delete_inline()
RETURNS TRIGGER AS $$
DECLARE
    pk_col text := TG_ARGV[0];
    pk_val integer;
BEGIN
    pk_val := (to_jsonb(OLD) ->> pk_col)::integer;
    EXECUTE format('UPDATE %I SET deleted_at = now() WHERE %I = $1', TG_TABLE_NAME, pk_col)
    USING pk_val;
    RETURN NULL; -- cancela o DELETE físico
END;
$$ LANGUAGE plpgsql;

-- Equivalente ao "ON UPDATE CURRENT_TIMESTAMP" do MySQL para maquinas.ultima_manutencao
CREATE OR REPLACE FUNCTION fn_touch_ultima_manutencao()
RETURNS TRIGGER AS $$
BEGIN
    NEW.ultima_manutencao := now();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Equivalente ao "ON UPDATE CURRENT_TIMESTAMP" do MySQL para solicitacoes_servico.atualizado_em
CREATE OR REPLACE FUNCTION fn_touch_atualizado_em()
RETURNS TRIGGER AS $$
BEGIN
    NEW.atualizado_em := now();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;
