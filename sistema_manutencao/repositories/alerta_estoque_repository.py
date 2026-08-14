from database.conexao import Conexao
from models.alerta_estoque import AlertaEstoque

class AlertaEstoqueRepository:
    """alertas_estoque usa soft delete por HERANÇA (ver notas em
    usuario_repository.py) — usa "FROM ONLY alertas_estoque".
    """

    def __init__(self):
        self.db = Conexao()

    def criar_alerta(self, registro):
        return AlertaEstoque(
            id_alerta=registro[0],
            item_id=registro[1],
            mensagem_alerta=registro[2],
            status=registro[3],
            criado_em=registro[4]
        )

    def criar_se_nao_existir(self, item_id, mensagem):
        """Evita duplicar alerta: só cria se não houver um Pendente pro mesmo item."""
        sql_verifica = """
            SELECT id_alerta
            FROM ONLY alertas_estoque
            WHERE item_id = %s AND status = 'Pendente'
        """
        try:
            self.db.cursor.execute(sql_verifica, (item_id,))
            existente = self.db.cursor.fetchone()

            if existente:
                return

            sql_inserir = """
                INSERT INTO alertas_estoque (item_id, mensagem_alerta)
                VALUES (%s, %s)
            """
            self.db.cursor.execute(sql_inserir, (item_id, mensagem))
            self.db.commit()
            print("Alerta de estoque gerado.")

        except Exception as erro:
            self.db.rollback()
            print(f"Erro ao gerar alerta de estoque: {erro}")

    def buscar_por_id(self, id_alerta):
        sql = """
        SELECT id_alerta, item_id, mensagem_alerta, status, criado_em
        FROM ONLY alertas_estoque
        WHERE id_alerta = %s
        """
        try:
            self.db.cursor.execute(sql, (id_alerta,))
            registro = self.db.cursor.fetchone()

            if registro is None:
                return None

            return self.criar_alerta(registro)

        except Exception as erro:
            print(f"Erro ao buscar alerta pelo id. Erro: {erro}")
            return None

    def listar(self):
        sql = """
            SELECT id_alerta, item_id, mensagem_alerta, status, criado_em
            FROM ONLY alertas_estoque
            ORDER BY criado_em DESC
        """
        try:
            self.db.cursor.execute(sql)
            registros = self.db.cursor.fetchall()
            alertas = []

            for registro in registros:
                alertas.append(self.criar_alerta(registro))
            return alertas

        except Exception as erro:
            print(f"Erro ao listar alertas: {erro}")
            return []

    def listar_pendentes(self):
        sql = """
            SELECT id_alerta, item_id, mensagem_alerta, status, criado_em
            FROM ONLY alertas_estoque
            WHERE status = 'Pendente'
            ORDER BY criado_em DESC
        """
        try:
            self.db.cursor.execute(sql)
            registros = self.db.cursor.fetchall()
            alertas = []

            for registro in registros:
                alertas.append(self.criar_alerta(registro))
            return alertas

        except Exception as erro:
            print(f"Erro ao listar alertas pendentes: {erro}")
            return []

    def resolver(self, id_alerta):
        sql = """
            UPDATE alertas_estoque
            SET status = 'Resolvido'
            WHERE id_alerta = %s
        """
        try:
            self.db.cursor.execute(sql, (id_alerta,))
            self.db.commit()

            if self.db.cursor.rowcount == 0:
                print("Alerta não encontrado!")

            else:
                print("Alerta resolvido!")

        except Exception as erro:
            self.db.rollback()
            print(f"Erro ao resolver alerta: {erro}")

    def excluir(self, id_alerta):
        sql = """
            DELETE FROM alertas_estoque
            WHERE id_alerta = %s
        """
        try:
            self.db.cursor.execute(sql, (id_alerta,))
            self.db.commit()

            if self.db.cursor.rowcount == 0:
                print("Alerta não encontrado!")

            else:
                print("Alerta excluído com sucesso!")

        except Exception as erro:
            self.db.rollback()
            print(f"Erro ao excluir alerta: {erro}")

    def fechar(self):
        self.db.fechar()
