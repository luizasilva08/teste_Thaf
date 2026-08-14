from database.conexao import obter_conexao
from models.alerta_estoque import AlertaEstoque
from repositories.base_repository import BaseRepository


class AlertaEstoqueRepository(BaseRepository):
    tabela = "alertas_estoque"
    colunas = ("item_id", "mensagem", "status")
    model_cls = AlertaEstoque

    def criar_se_nao_existir(self, item_id: int, mensagem: str) -> int | None:
        sql = "SELECT id FROM alertas_estoque WHERE item_id = %s AND status = 'Pendente'"
        conn = obter_conexao()
        try:
            cursor = conn.cursor()
            cursor.execute(sql, (item_id,))
            existente = cursor.fetchone()
            cursor.close()
        finally:
            conn.close()

        if existente:
            return None

        return self.criar(AlertaEstoque(item_id=item_id, mensagem=mensagem))

    def listar_pendentes(self):
        return self.listar(filtros={"status": "Pendente"})

    def resolver(self, id_: int) -> bool:
        sql = "UPDATE alertas_estoque SET status = 'Resolvido' WHERE id = %s"
        conn = obter_conexao()
        try:
            cursor = conn.cursor()
            cursor.execute(sql, (id_,))
            conn.commit()
            afetadas = cursor.rowcount
            cursor.close()
            return afetadas > 0
        finally:
            conn.close()
