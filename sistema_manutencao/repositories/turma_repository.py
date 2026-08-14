from database.conexao import Conexao
from models.turma import Turma

class TurmaRepository:
    def __init__(self):
        self.db = Conexao()

    def criar_turma(self, registro):
        return Turma(
            id_turma=registro[0],
            codigo=registro[1],
            periodo=registro[2]
        )

    def salvar(self, turma):
        sql = """
        INSERT INTO turmas
        (
            codigo,
            periodo
        )
        VALUES
        (
            %s, %s
        )
        """
        valores = (
            turma.codigo,
            turma.periodo
        )
        try:
            self.db.cursor.execute(sql, valores)
            self.db.commit()
            print("Turma cadastrada com sucesso!")

        except Exception as erro:
            self.db.rollback()
            print(f"Erro ao cadastrar turma. Erro: {erro}")

    def buscar_por_id(self, id_turma):
        sql = """
        SELECT *
        FROM turmas
        WHERE id = %s
        """
        try:
            self.db.cursor.execute(sql, (id_turma,))
            registro = self.db.cursor.fetchone()

            if registro is None:
                return None

            return self.criar_turma(registro)

        except Exception as erro:
            print(f"Erro ao buscar turma pelo id. Erro: {erro}")
            return None

    def listar(self):
        sql = """
            SELECT *
            FROM turmas
            ORDER BY codigo
        """
        try:
            self.db.cursor.execute(sql)
            registros = self.db.cursor.fetchall()
            turmas = []

            for registro in registros:
                turmas.append(self.criar_turma(registro))
            return turmas

        except Exception as erro:
            print(f"Erro ao listar turmas: {erro}")
            return []

    def atualizar(self, turma):
        sql = """UPDATE turmas
        SET
            codigo = %s,
            periodo = %s
        WHERE id = %s
        """
        valores = (
            turma.codigo,
            turma.periodo,
            turma.id_turma
        )
        try:
            self.db.cursor.execute(sql, valores)
            self.db.commit()
            if self.db.cursor.rowcount == 0:
                print("Turma não encontrada!")

            else:
                print("Turma atualizada!")

        except Exception as erro:
            self.db.rollback()
            print(f"Erro ao atualizar turma: {erro}")

    def excluir(self, id_turma):
        sql = """
            DELETE FROM turmas
            WHERE id = %s
        """
        try:
            self.db.cursor.execute(sql, (id_turma,))
            self.db.commit()

            if self.db.cursor.rowcount == 0:
                print("Turma não encontrada!")

            else:
                print("Turma excluída com sucesso!")

        except Exception as erro:
            self.db.rollback()
            print(f"Erro ao excluir turma: {erro}")

    def fechar(self):
        self.db.fechar()
