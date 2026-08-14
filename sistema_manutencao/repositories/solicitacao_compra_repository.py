from database.conexao import obter_conexao
from models.solicitacao_compra import SolicitacaoCompra
from repositories.base_repository import BaseRepository


class SolicitacaoCompraRepository(BaseRepository):
    tabela = "solicitacoes_compras"
    colunas = (
        "solicitante_id",
        "professor_responsavel_id",
        "turma_id",
        "maquina_id",
        "status",
        "especificacao_tecnica",
        "quantidade",
        "sap",
        "justificativa",
        "patrimonio",
        "equipamento",
        "conjunto_mecanico",
        "arquivos",
    )
    model_cls = SolicitacaoCompra

    def listar_por_status(self, status: str):
        return self.listar(filtros={"status": status})

    def listar_por_turma(self, turma_id: int):
        return self.listar(filtros={"turma_id": turma_id})

    def atualizar_status(self, id_: int, status: str) -> bool:
        sql = "UPDATE solicitacoes_compras SET status = %s WHERE id = %s"
        conn = obter_conexao()
        try:
            cursor = conn.cursor()
            cursor.execute(sql, (status, id_))
            conn.commit()
            afetadas = cursor.rowcount
            cursor.close()
            return afetadas > 0
        finally:
            conn.close()
