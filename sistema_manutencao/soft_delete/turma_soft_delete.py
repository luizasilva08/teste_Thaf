from database.conexao import Conexao
from models.turma import Turma

class TurmaSoftDelete:
    """Operações sobre turmas EXCLUÍDAS (deleted_at IS NOT NULL).

    turmas usa soft delete IN-PLACE, igual perfis (ver notas em
    perfil_soft_delete.py). Não existe "excluir_definitivamente" pelo
    mesmo motivo: o trigger trg_soft_delete_turmas intercepta qualquer
    DELETE na tabela, mesmo em linha já excluída.
    """

    def __init__(self):
        self.db = Conexao()

    def criar_turma(self, registro):
        return Turma(
            id_turma=registro[0],
            codigo_turma=registro[1],
            periodo_turma=registro[2],
            deleted_at=registro[3]
        )

    def listar_excluidos(self):
        sql = """
            SELECT id_turma, codigo_turma, periodo_turma, deleted_at
            FROM turmas
            WHERE deleted_at IS NOT NULL
            ORDER BY deleted_at DESC
        """
        try:
            self.db.cursor.execute(sql)
            registros = self.db.cursor.fetchall()
            turmas = []

            for registro in registros:
                turmas.append(self.criar_turma(registro))
            return turmas

        except Exception as erro:
            print(f"Erro ao listar turmas excluídas: {erro}")
            return []

    def buscar_excluido_por_id(self, id_turma):
        sql = """
            SELECT id_turma, codigo_turma, periodo_turma, deleted_at
            FROM turmas
            WHERE id_turma = %s AND deleted_at IS NOT NULL
        """
        try:
            self.db.cursor.execute(sql, (id_turma,))
            registro = self.db.cursor.fetchone()

            if registro is None:
                return None

            return self.criar_turma(registro)

        except Exception as erro:
            print(f"Erro ao buscar turma excluída pelo id. Erro: {erro}")
            return None

    def restaurar(self, id_turma):
        if self.buscar_excluido_por_id(id_turma) is None:
            print("Turma excluída não encontrada!")
            return

        sql = """
            UPDATE turmas
            SET deleted_at = NULL
            WHERE id_turma = %s AND deleted_at IS NOT NULL
        """
        try:
            self.db.cursor.execute(sql, (id_turma,))
            self.db.commit()
            print("Turma restaurada com sucesso!")

        except Exception as erro:
            self.db.rollback()
            print(f"Erro ao restaurar turma: {erro}")

    def fechar(self):
        self.db.fechar()
