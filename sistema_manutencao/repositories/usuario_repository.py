from database.conexao import Conexao
from models.usuario import Usuario

class UsuarioRepository:
    """usuarios usa soft delete por HERANÇA: DELETE move a linha para
    usuarios_deletados (trigger trg_soft_delete_usuarios). Toda consulta
    usa "FROM ONLY usuarios" para não trazer linhas já excluídas — sem o
    ONLY, o Postgres também retornaria as linhas da tabela filha.
    """

    def __init__(self):
        self.db = Conexao()

    def criar_usuario(self, registro):
        return Usuario(
            id_usuario=registro[0],
            perfil_id=registro[1],
            turma_id=registro[2],
            nome_usuario=registro[3],
            email_usuario=registro[4],
            senha_hash=registro[5],
            criado_em=registro[6]
        )

    def salvar(self, usuario):
        sql = """
        INSERT INTO usuarios
        (
            perfil_id,
            turma_id,
            nome_usuario,
            email_usuario,
            senha_hash
        )
        VALUES
        (
            %s, %s, %s, %s, %s
        )
        """
        valores = (
            usuario.perfil_id,
            usuario.turma_id,
            usuario.nome_usuario,
            usuario.email_usuario,
            usuario.senha_hash
        )
        try:
            self.db.cursor.execute(sql, valores)
            self.db.commit()
            print("Usuário cadastrado com sucesso!")

        except Exception as erro:
            self.db.rollback()
            print(f"Erro ao cadastrar usuário. Erro: {erro}")

    def buscar_por_id(self, id_usuario):
        sql = """
        SELECT id_usuario, perfil_id, turma_id, nome_usuario, email_usuario, senha_hash, criado_em
        FROM ONLY usuarios
        WHERE id_usuario = %s
        """
        try:
            self.db.cursor.execute(sql, (id_usuario,))
            registro = self.db.cursor.fetchone()

            if registro is None:
                return None

            return self.criar_usuario(registro)

        except Exception as erro:
            print(f"Erro ao buscar usuário pelo id. Erro: {erro}")
            return None

    def buscar_por_email(self, email_usuario):
        sql = """
        SELECT id_usuario, perfil_id, turma_id, nome_usuario, email_usuario, senha_hash, criado_em
        FROM ONLY usuarios
        WHERE email_usuario = %s
        """
        try:
            self.db.cursor.execute(sql, (email_usuario,))
            registro = self.db.cursor.fetchone()

            if registro is None:
                return None

            return self.criar_usuario(registro)

        except Exception as erro:
            print(f"Erro ao buscar usuário pelo e-mail. Erro: {erro}")
            return None

    def listar(self):
        sql = """
            SELECT id_usuario, perfil_id, turma_id, nome_usuario, email_usuario, senha_hash, criado_em
            FROM ONLY usuarios
            ORDER BY nome_usuario
        """
        try:
            self.db.cursor.execute(sql)
            registros = self.db.cursor.fetchall()
            usuarios = []

            for registro in registros:
                usuarios.append(self.criar_usuario(registro))
            return usuarios

        except Exception as erro:
            print(f"Erro ao listar usuários: {erro}")
            return []

    def listar_por_perfil(self, perfil_id):
        sql = """
            SELECT id_usuario, perfil_id, turma_id, nome_usuario, email_usuario, senha_hash, criado_em
            FROM ONLY usuarios
            WHERE perfil_id = %s
            ORDER BY nome_usuario
        """
        try:
            self.db.cursor.execute(sql, (perfil_id,))
            registros = self.db.cursor.fetchall()
            usuarios = []

            for registro in registros:
                usuarios.append(self.criar_usuario(registro))
            return usuarios

        except Exception as erro:
            print(f"Erro ao listar usuários por perfil: {erro}")
            return []

    def atualizar(self, usuario):
        sql = """UPDATE usuarios
        SET
            perfil_id = %s,
            turma_id = %s,
            nome_usuario = %s,
            email_usuario = %s,
            senha_hash = %s
        WHERE id_usuario = %s
        """
        valores = (
            usuario.perfil_id,
            usuario.turma_id,
            usuario.nome_usuario,
            usuario.email_usuario,
            usuario.senha_hash,
            usuario.id_usuario
        )
        try:
            self.db.cursor.execute(sql, valores)
            self.db.commit()
            if self.db.cursor.rowcount == 0:
                print("Usuário não encontrado!")

            else:
                print("Usuário atualizado!")

        except Exception as erro:
            self.db.rollback()
            print(f"Erro ao atualizar usuário: {erro}")

    def excluir(self, id_usuario):
        sql = """
            DELETE FROM usuarios
            WHERE id_usuario = %s
        """
        try:
            self.db.cursor.execute(sql, (id_usuario,))
            self.db.commit()

            if self.db.cursor.rowcount == 0:
                print("Usuário não encontrado!")

            else:
                print("Usuário excluído com sucesso!")

        except Exception as erro:
            self.db.rollback()
            print(f"Erro ao excluir usuário: {erro}")

    def fechar(self):
        self.db.fechar()
