from database.conexao import Conexao
from models.ordem_servico import OrdemServico

class OrdemServicoRepository:
    """ordens_servico usa soft delete por HERANÇA (ver notas em
    usuario_repository.py) — usa "FROM ONLY ordens_servico".
    """

    def __init__(self):
        self.db = Conexao()

    def criar_ordem(self, registro):
        return OrdemServico(
            id_os=registro[0],
            solicitacao_id=registro[1],
            maquina_id=registro[2],
            turma_id=registro[3],
            tipo_manutencao=registro[4],
            criticidade_os=registro[5],
            descricao_execucao=registro[6],
            pecas_usadas=registro[7],
            data_execucao=registro[8],
            hora_inicio=registro[9],
            hora_fim=registro[10],
            quantidade_pessoas=registro[11],
            criado_em=registro[12]
        )

    def salvar(self, ordem):
        sql = """
        INSERT INTO ordens_servico
        (
            solicitacao_id,
            maquina_id,
            turma_id,
            tipo_manutencao,
            criticidade_os,
            descricao_execucao,
            pecas_usadas,
            data_execucao,
            hora_inicio,
            hora_fim,
            quantidade_pessoas
        )
        VALUES
        (
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
        )
        """
        valores = (
            ordem.solicitacao_id,
            ordem.maquina_id,
            ordem.turma_id,
            ordem.tipo_manutencao,
            ordem.criticidade_os,
            ordem.descricao_execucao,
            ordem.pecas_usadas,
            ordem.data_execucao,
            ordem.hora_inicio,
            ordem.hora_fim,
            ordem.quantidade_pessoas
        )
        try:
            self.db.cursor.execute(sql, valores)
            self.db.commit()
            print("Ordem de serviço cadastrada com sucesso!")

        except Exception as erro:
            self.db.rollback()
            print(f"Erro ao cadastrar ordem de serviço. Erro: {erro}")

    def abrir_a_partir_de_ss(self, solicitacao_id, tipo_manutencao, criticidade_os,
                              descricao_execucao, data_execucao, hora_inicio, hora_fim,
                              pecas_usadas=None, quantidade_pessoas=1, turma_id=None):
        """Cria a OS vinculada a uma SS, conclui a SS e volta a máquina pra 'Operando'."""
        from repositories.maquina_repository import MaquinaRepository
        from repositories.solicitacao_servico_repository import SolicitacaoServicoRepository

        solicitacoes = SolicitacaoServicoRepository()
        solicitacao = solicitacoes.buscar_por_id(solicitacao_id)
        if solicitacao is None:
            solicitacoes.fechar()
            raise ValueError(f"Solicitação {solicitacao_id} não encontrada.")

        ordem = OrdemServico(
            solicitacao_id=solicitacao_id,
            maquina_id=solicitacao.maquina_id,
            turma_id=turma_id,
            tipo_manutencao=tipo_manutencao,
            criticidade_os=criticidade_os,
            descricao_execucao=descricao_execucao,
            pecas_usadas=pecas_usadas,
            data_execucao=data_execucao,
            hora_inicio=hora_inicio,
            hora_fim=hora_fim,
            quantidade_pessoas=quantidade_pessoas
        )
        self.salvar(ordem)

        # A execução da OS conclui a SS, mas o status da SS só anda um passo
        # de cada vez (ver TRANSICOES_PERMITIDAS) — percorre o caminho até
        # 'Concluída' a partir de onde a SS estiver.
        caminho_ate_concluida = {
            "Aberta": ["Em Análise", "Execução", "Validação", "Concluída"],
            "Em Análise": ["Execução", "Validação", "Concluída"],
            "Aguardando Peças": ["Execução", "Validação", "Concluída"],
            "Execução": ["Validação", "Concluída"],
            "Validação": ["Concluída"],
            "Concluída": [],
        }
        for proximo_status in caminho_ate_concluida.get(solicitacao.status, []):
            solicitacoes.atualizar_status(solicitacao_id, proximo_status)
        solicitacoes.fechar()

        maquinas = MaquinaRepository()
        maquinas.registrar_manutencao_concluida(solicitacao.maquina_id)
        maquinas.fechar()

    def buscar_por_id(self, id_os):
        sql = """
        SELECT id_os, solicitacao_id, maquina_id, turma_id, tipo_manutencao, criticidade_os,
               descricao_execucao, pecas_usadas, data_execucao, hora_inicio, hora_fim,
               quantidade_pessoas, criado_em
        FROM ONLY ordens_servico
        WHERE id_os = %s
        """
        try:
            self.db.cursor.execute(sql, (id_os,))
            registro = self.db.cursor.fetchone()

            if registro is None:
                return None

            return self.criar_ordem(registro)

        except Exception as erro:
            print(f"Erro ao buscar ordem de serviço pelo id. Erro: {erro}")
            return None

    def listar(self):
        sql = """
            SELECT id_os, solicitacao_id, maquina_id, turma_id, tipo_manutencao, criticidade_os,
                   descricao_execucao, pecas_usadas, data_execucao, hora_inicio, hora_fim,
                   quantidade_pessoas, criado_em
            FROM ONLY ordens_servico
            ORDER BY data_execucao DESC
        """
        try:
            self.db.cursor.execute(sql)
            registros = self.db.cursor.fetchall()
            ordens = []

            for registro in registros:
                ordens.append(self.criar_ordem(registro))
            return ordens

        except Exception as erro:
            print(f"Erro ao listar ordens de serviço: {erro}")
            return []

    def listar_por_maquina(self, maquina_id):
        sql = """
            SELECT id_os, solicitacao_id, maquina_id, turma_id, tipo_manutencao, criticidade_os,
                   descricao_execucao, pecas_usadas, data_execucao, hora_inicio, hora_fim,
                   quantidade_pessoas, criado_em
            FROM ONLY ordens_servico
            WHERE maquina_id = %s
            ORDER BY data_execucao DESC
        """
        try:
            self.db.cursor.execute(sql, (maquina_id,))
            registros = self.db.cursor.fetchall()
            ordens = []

            for registro in registros:
                ordens.append(self.criar_ordem(registro))
            return ordens

        except Exception as erro:
            print(f"Erro ao listar ordens de serviço por máquina: {erro}")
            return []

    def excluir(self, id_os):
        sql = """
            DELETE FROM ordens_servico
            WHERE id_os = %s
        """
        try:
            self.db.cursor.execute(sql, (id_os,))
            self.db.commit()

            if self.db.cursor.rowcount == 0:
                print("Ordem de serviço não encontrada!")

            else:
                print("Ordem de serviço excluída com sucesso!")

        except Exception as erro:
            self.db.rollback()
            print(f"Erro ao excluir ordem de serviço: {erro}")

    def fechar(self):
        self.db.fechar()
