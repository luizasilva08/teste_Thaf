from models.ordem_servico import OrdemServico
from repositories.base_repository import BaseRepository
from repositories.maquina_repository import MaquinaRepository
from repositories.solicitacao_servico_repository import SolicitacaoServicoRepository


class OrdemServicoRepository(BaseRepository):
    tabela = "ordens_servico"
    colunas = (
        "solicitacao_id",
        "maquina_id",
        "turma_id",
        "tipo_manutencao",
        "criticidade",
        "descricao_execucao",
        "pecas_usadas",
        "data_execucao",
        "hora_inicio",
        "hora_fim",
        "quantidade_pessoas",
    )
    model_cls = OrdemServico

    def abrir_a_partir_de_ss(self, solicitacao_id: int, **dados_execucao) -> int:
        """Cria a OS vinculada a uma SS e conclui a SS."""
        solicitacoes = SolicitacaoServicoRepository()
        solicitacao = solicitacoes.buscar_por_id(solicitacao_id)
        if solicitacao is None:
            raise ValueError(f"Solicitação {solicitacao_id} não encontrada.")

        ordem = OrdemServico(
            solicitacao_id=solicitacao_id,
            maquina_id=solicitacao.maquina_id,
            **dados_execucao,
        )
        novo_id = self.criar(ordem)

        MaquinaRepository().registrar_manutencao_concluida(solicitacao.maquina_id)
        return novo_id

    def listar_por_maquina(self, maquina_id: int):
        return self.listar(filtros={"maquina_id": maquina_id})
