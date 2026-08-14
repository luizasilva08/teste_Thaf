from database.conexao import obter_conexao
from models.solicitacao_servico import TRANSICOES_PERMITIDAS, SolicitacaoServico
from repositories.base_repository import BaseRepository


class TransicaoInvalidaError(Exception):
    pass


class SolicitacaoServicoRepository(BaseRepository):
    tabela = "solicitacoes_servico"
    colunas = (
        "maquina_id",
        "solicitante_id",
        "responsavel_id",
        "professor_validador_id",
        "descricao_problema",
        "prioridade_ss",
        "tipo_manutencao",
        "status",
    )
    model_cls = SolicitacaoServico

    def listar_por_status(self, status: str):
        return self.listar(filtros={"status": status})

    def listar_por_maquina(self, maquina_id: int):
        return self.listar(filtros={"maquina_id": maquina_id})

    def listar_por_solicitante(self, solicitante_id: int):
        return self.listar(filtros={"solicitante_id": solicitante_id})

    def atualizar_status(self, id_: int, novo_status: str) -> SolicitacaoServico:
        atual = self.buscar_por_id(id_)
        if atual is None:
            raise ValueError(f"Solicitação {id_} não encontrada.")

        permitidas = TRANSICOES_PERMITIDAS.get(atual.status, set())
        if novo_status not in permitidas:
            raise TransicaoInvalidaError(
                f"Não é possível mudar de '{atual.status}' para '{novo_status}'."
            )

        sql = "UPDATE solicitacoes_servico SET status = %s WHERE id = %s"
        conn = obter_conexao()
        try:
            cursor = conn.cursor()
            cursor.execute(sql, (novo_status, id_))
            conn.commit()
            cursor.close()
        finally:
            conn.close()

        return self.buscar_por_id(id_)

    def atribuir_responsavel(self, id_: int, responsavel_id: int) -> bool:
        sql = "UPDATE solicitacoes_servico SET responsavel_id = %s WHERE id = %s"
        conn = obter_conexao()
        try:
            cursor = conn.cursor()
            cursor.execute(sql, (responsavel_id, id_))
            conn.commit()
            afetadas = cursor.rowcount
            cursor.close()
            return afetadas > 0
        finally:
            conn.close()
