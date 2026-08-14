from database.conexao import Conexao
from models.perfil import Perfil

class PerfilRepository:
    def __init__(self):
        self.db = Conexao()

    def criar_perfil(self, registro):
        return Perfil(
            id_perfil=registro[0],
            nome=registro[1],
            descricao=registro[2]
        )

    def salvar(self, perfil):
        sql = """
        INSERT INTO perfis
        (
            nome,
            descricao
        )
        VALUES
        (
            %s, %s
        )
        """
        valores = (
            perfil.nome,
            perfil.descricao
        )
        try:
            self.db.cursor.execute(sql, valores)
            self.db.commit()
            print("Perfil cadastrado com sucesso!")

        except Exception as erro:
            self.db.rollback()
            print(f"Erro ao cadastrar perfil. Erro: {erro}")

    def buscar_por_id(self, id_perfil):
        sql = """
        SELECT *
        FROM perfis
        WHERE id = %s
        """
        try:
            self.db.cursor.execute(sql, (id_perfil,))
            registro = self.db.cursor.fetchone()

            if registro is None:
                return None

            return self.criar_perfil(registro)

        except Exception as erro:
            print(f"Erro ao buscar perfil pelo id. Erro: {erro}")
            return None

    def listar(self):
        sql = """
            SELECT *
            FROM perfis
            ORDER BY nome
        """
        try:
            self.db.cursor.execute(sql)
            registros = self.db.cursor.fetchall()
            perfis = []

            for registro in registros:
                perfis.append(self.criar_perfil(registro))
            return perfis

        except Exception as erro:
            print(f"Erro ao listar perfis: {erro}")
            return []

    def atualizar(self, perfil):
        sql = """UPDATE perfis
        SET
            nome = %s,
            descricao = %s
        WHERE id = %s
        """
        valores = (
            perfil.nome,
            perfil.descricao,
            perfil.id_perfil
        )
        try:
            self.db.cursor.execute(sql, valores)
            self.db.commit()
            if self.db.cursor.rowcount == 0:
                print("Perfil não encontrado!")

            else:
                print("Perfil atualizado!")

        except Exception as erro:
            self.db.rollback()
            print(f"Erro ao atualizar perfil: {erro}")

    def excluir(self, id_perfil):
        sql = """
            DELETE FROM perfis
            WHERE id = %s
        """
        try:
            self.db.cursor.execute(sql, (id_perfil,))
            self.db.commit()

            if self.db.cursor.rowcount == 0:
                print("Perfil não encontrado!")

            else:
                print("Perfil excluído com sucesso!")

        except Exception as erro:
            self.db.rollback()
            print(f"Erro ao excluir perfil: {erro}")

    def fechar(self):
        self.db.fechar()
