CREATE TABLE perfis (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(50) NOT NULL UNIQUE,
    descricao TEXT,
    CONSTRAINT chk_perfil_nome CHECK (
        LOWER(nome) IN ('coordenador', 'gestor', 'professor', 'aluno', 'representante')
    )
);
