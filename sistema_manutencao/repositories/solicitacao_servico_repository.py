from database.conexao import Conexao
from models.solicitacao_servico import TRANSICOES_PERMITIDAS, SolicitacaoServico


class TransicaoInvalidaError(Exception):
    pass


class SolicitacaoServicoRepository:
    """solicitacoes_servico usa soft delete por HERANÇA (ver notas em
    usuario_repository.py) — usa "FROM ONLY solicitacoes_servico". O
    trigger trg_touch_solicitacoes_servico já atualiza atualizado_em = now()
    sozinho em qualquer UPDATE.
    """

    def __init__(self):
        self.db = Conexao()

    def criar_solicitacao(self, registro):
        return SolicitacaoServico(
            id_ss=registro[0],
            maquina_id=registro[1],
            solicitante_id=registro[2],
            responsavel_id=registro[3],
            professor_validador_id=registro[4],
            descricao_problema=registro[5],
            prioridade_ss=registro[6],
            tipo_manutencao=registro[7],
            status=registro[8],
            criado_em=registro[9],
            atualizado_em=registro[10]
        )

    def salvar(self, solicitacao):
        sql = """
        INSERT INTO solicitacoes_servico
        (
            maquina_id,
            solicitante_id,
            responsavel_id,
            professor_validador_id,
            descricao_problema,
            prioridade_ss,
            tipo_manutencao
        )
        VALUES
        (
            %s, %s, %s, %s, %s, %s, %s
        )
        """
        valores = (
            solicitacao.maquina_id,
            solicitacao.solicitante_id,
            solicitacao.responsavel_id,
            solicitacao.professor_validador_id,
            solicitacao.descricao_problema,
            solicitacao.prioridade_ss,
            solicitacao.tipo_manutencao
        )
        try:
            self.db.cursor.execute(sql, valores)
            self.db.commit()
            print("Solicitação de serviço cadastrada com sucesso!")

        except Exception as erro:
            self.db.rollback()
            print(f"Erro ao cadastrar solicitação de serviço. Erro: {erro}")

    def buscar_por_id(self, id_ss):
        sql = """
        SELECT id_ss, maquina_id, solicitante_id, responsavel_id, professor_validador_id,
               descricao_problema, prioridade_ss, tipo_manutencao, status, criado_em, atualizado_em
        FROM ONLY solicitacoes_servico
        WHERE id_ss = %s
        """
        try:
            self.db.cursor.execute(sql, (id_ss,))
            registro = self.db.cursor.fetchone()

            if registro is None:
                return None

            return self.criar_solicitacao(registro)

        except Exception as erro:
            print(f"Erro ao buscar solicitação pelo id. Erro: {erro}")
            return None

    def listar(self):
        sql = """
            SELECT id_ss, maquina_id, solicitante_id, responsavel_id, professor_validador_id,
                   descricao_problema, prioridade_ss, tipo_manutencao, status, criado_em, atualizado_em
            FROM ONLY solicitacoes_servico
            ORDER BY criado_em DESC
        """
        try:
            self.db.cursor.execute(sql)
            registros = self.db.cursor.fetchall()
            solicitacoes = []

            for registro in registros:
                solicitacoes.append(self.criar_solicitacao(registro))
            return solicitacoes

        except Exception as erro:
            print(f"Erro ao listar solicitações: {erro}")
            return []

    def listar_por_status(self, status):
        sql = """
            SELECT id_ss, maquina_id, solicitante_id, responsavel_id, professor_validador_id,
                   descricao_problema, prioridade_ss, tipo_manutencao, status, criado_em, atualizado_em
            FROM ONLY solicitacoes_servico
            WHERE status = %s
            ORDER BY criado_em DESC
        """
        try:
            self.db.cursor.execute(sql, (status,))
            registros = self.db.cursor.fetchall()
            solicitacoes = []

            for registro in registros:
                solicitacoes.append(self.criar_solicitacao(registro))
            return solicitacoes

        except Exception as erro:
            print(f"Erro ao listar solicitações por status: {erro}")
            return []

    def listar_por_maquina(self, maquina_id):
        sql = """
            SELECT id_ss, maquina_id, solicitante_id, responsavel_id, professor_validador_id,
                   descricao_problema, prioridade_ss, tipo_manutencao, status, criado_em, atualizado_em
            FROM ONLY solicitacoes_servico
            WHERE maquina_id = %s
            ORDER BY criado_em DESC
        """
        try:
            self.db.cursor.execute(sql, (maquina_id,))
            registros = self.db.cursor.fetchall()
            solicitacoes = []

            for registro in registros:
                solicitacoes.append(self.criar_solicitacao(registro))
            return solicitacoes

        except Exception as erro:
            print(f"Erro ao listar solicitações por máquina: {erro}")
            return []

    def atualizar_status(self, id_ss, novo_status):
        atual = self.buscar_por_id(id_ss)
        if atual is None:
            raise ValueError(f"Solicitação {id_ss} não encontrada.")

        permitidas = TRANSICOES_PERMITIDAS.get(atual.status, set())
        if novo_status not in permitidas:
            raise TransicaoInvalidaError(
                f"Não é possível mudar de '{atual.status}' para '{novo_status}'."
            )

        sql = """
            UPDATE solicitacoes_servico
            SET status = %s
            WHERE id_ss = %s
        """
        try:
            self.db.cursor.execute(sql, (novo_status, id_ss))
            self.db.commit()
            print("Status atualizado!")

        except Exception as erro:
            self.db.rollback()
            print(f"Erro ao atualizar status: {erro}")

    def atribuir_responsavel(self, id_ss, responsavel_id):
        sql = """
            UPDATE solicitacoes_servico
            SET responsavel_id = %s
            WHERE id_ss = %s
        """
        try:
            self.db.cursor.execute(sql, (responsavel_id, id_ss))
            self.db.commit()

            if self.db.cursor.rowcount == 0:
                print("Solicitação não encontrada!")

            else:
                print("Responsável atribuído!")

        except Exception as erro:
            self.db.rollback()
            print(f"Erro ao atribuir responsável: {erro}")

    def excluir(self, id_ss):
        sql = """
            DELETE FROM solicitacoes_servico
            WHERE id_ss = %s
        """
        try:
            self.db.cursor.execute(sql, (id_ss,))
            self.db.commit()

            if self.db.cursor.rowcount == 0:
                print("Solicitação não encontrada!")

            else:
                print("Solicitação excluída com sucesso!")

        except Exception as erro:
            self.db.rollback()
            print(f"Erro ao excluir solicitação: {erro}")

    def fechar(self):
        self.db.fechar()
