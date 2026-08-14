from database.conexao import Conexao
from models.setor import Setor

class SetorRepository:
    def __init__(self):
        self.db = Conexao()

    def criar_setor(self, registro):
        return Setor(
            id_setor=registro[0],
            nome=registro[1],
            descricao=registro[2]
        )

    def salvar(self, setor):
        sql = """
        INSERT INTO setores
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
            setor.nome,
            setor.descricao
        )
        try:
            self.db.cursor.execute(sql, valores)
            self.db.commit()
            print("Setor cadastrado com sucesso!")

        except Exception as erro:
            self.db.rollback()
            print(f"Erro ao cadastrar setor. Erro: {erro}")

    def buscar_por_id(self, id_setor):
        sql = """
        SELECT *
        FROM setores
        WHERE id = %s
        """
        try:
            self.db.cursor.execute(sql, (id_setor,))
            registro = self.db.cursor.fetchone()

            if registro is None:
                return None

            return self.criar_setor(registro)

        except Exception as erro:
            print(f"Erro ao buscar setor pelo id. Erro: {erro}")
            return None

    def listar(self):
        sql = """
            SELECT *
            FROM setores
            ORDER BY nome
        """
        try:
            self.db.cursor.execute(sql)
            registros = self.db.cursor.fetchall()
            setores = []

            for registro in registros:
                setores.append(self.criar_setor(registro))
            return setores

        except Exception as erro:
            print(f"Erro ao listar setores: {erro}")
            return []

    def atualizar(self, setor):
        sql = """UPDATE setores
        SET
            nome = %s,
            descricao = %s
        WHERE id = %s
        """
        valores = (
            setor.nome,
            setor.descricao,
            setor.id_setor
        )
        try:
            self.db.cursor.execute(sql, valores)
            self.db.commit()
            if self.db.cursor.rowcount == 0:
                print("Setor não encontrado!")

            else:
                print("Setor atualizado!")

        except Exception as erro:
            self.db.rollback()
            print(f"Erro ao atualizar setor: {erro}")

    def excluir(self, id_setor):
        sql = """
            DELETE FROM setores
            WHERE id = %s
        """
        try:
            self.db.cursor.execute(sql, (id_setor,))
            self.db.commit()

            if self.db.cursor.rowcount == 0:
                print("Setor não encontrado!")

            else:
                print("Setor excluído com sucesso!")

        except Exception as erro:
            self.db.rollback()
            print(f"Erro ao excluir setor: {erro}")

    def fechar(self):
        self.db.fechar()
