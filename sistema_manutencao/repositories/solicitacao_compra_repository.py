from database.conexao import Conexao
from models.solicitacao_compra import SolicitacaoCompra

class SolicitacaoCompraRepository:
    """solicitacoes_compras usa soft delete por HERANÇA (ver notas em
    usuario_repository.py) — usa "FROM ONLY solicitacoes_compras".
    """

    def __init__(self):
        self.db = Conexao()

    def criar_solicitacao(self, registro):
        return SolicitacaoCompra(
            id_solicitacao=registro[0],
            solicitante_id=registro[1],
            professor_responsavel_id=registro[2],
            turma_id=registro[3],
            maquina_id=registro[4],
            status=registro[5],
            especificacao_tecnica=registro[6],
            quantidade_solicitacao=registro[7],
            sap_solicitacao=registro[8],
            justificativa_solicitacao=registro[9],
            patrimonio=registro[10],
            equipamento=registro[11],
            conjunto_mecanico=registro[12],
            arquivos=registro[13],
            criado_em=registro[14]
        )

    def salvar(self, solicitacao):
        sql = """
        INSERT INTO solicitacoes_compras
        (
            solicitante_id,
            professor_responsavel_id,
            turma_id,
            maquina_id,
            especificacao_tecnica,
            quantidade_solicitacao,
            sap_solicitacao,
            justificativa_solicitacao,
            patrimonio,
            equipamento,
            conjunto_mecanico,
            arquivos
        )
        VALUES
        (
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
        )
        """
        valores = (
            solicitacao.solicitante_id,
            solicitacao.professor_responsavel_id,
            solicitacao.turma_id,
            solicitacao.maquina_id,
            solicitacao.especificacao_tecnica,
            solicitacao.quantidade_solicitacao,
            solicitacao.sap_solicitacao,
            solicitacao.justificativa_solicitacao,
            solicitacao.patrimonio,
            solicitacao.equipamento,
            solicitacao.conjunto_mecanico,
            solicitacao.arquivos
        )
        try:
            self.db.cursor.execute(sql, valores)
            self.db.commit()
            print("Solicitação de compra cadastrada com sucesso!")

        except Exception as erro:
            self.db.rollback()
            print(f"Erro ao cadastrar solicitação de compra. Erro: {erro}")

    def buscar_por_id(self, id_solicitacao):
        sql = """
        SELECT id_solicitacao, solicitante_id, professor_responsavel_id, turma_id, maquina_id,
               status, especificacao_tecnica, quantidade_solicitacao, sap_solicitacao,
               justificativa_solicitacao, patrimonio, equipamento, conjunto_mecanico, arquivos, criado_em
        FROM ONLY solicitacoes_compras
        WHERE id_solicitacao = %s
        """
        try:
            self.db.cursor.execute(sql, (id_solicitacao,))
            registro = self.db.cursor.fetchone()

            if registro is None:
                return None

            return self.criar_solicitacao(registro)

        except Exception as erro:
            print(f"Erro ao buscar solicitação de compra pelo id. Erro: {erro}")
            return None

    def listar(self):
        sql = """
            SELECT id_solicitacao, solicitante_id, professor_responsavel_id, turma_id, maquina_id,
                   status, especificacao_tecnica, quantidade_solicitacao, sap_solicitacao,
                   justificativa_solicitacao, patrimonio, equipamento, conjunto_mecanico, arquivos, criado_em
            FROM ONLY solicitacoes_compras
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
            print(f"Erro ao listar solicitações de compra: {erro}")
            return []

    def listar_por_status(self, status):
        sql = """
            SELECT id_solicitacao, solicitante_id, professor_responsavel_id, turma_id, maquina_id,
                   status, especificacao_tecnica, quantidade_solicitacao, sap_solicitacao,
                   justificativa_solicitacao, patrimonio, equipamento, conjunto_mecanico, arquivos, criado_em
            FROM ONLY solicitacoes_compras
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
            print(f"Erro ao listar solicitações de compra por status: {erro}")
            return []

    def listar_por_turma(self, turma_id):
        sql = """
            SELECT id_solicitacao, solicitante_id, professor_responsavel_id, turma_id, maquina_id,
                   status, especificacao_tecnica, quantidade_solicitacao, sap_solicitacao,
                   justificativa_solicitacao, patrimonio, equipamento, conjunto_mecanico, arquivos, criado_em
            FROM ONLY solicitacoes_compras
            WHERE turma_id = %s
            ORDER BY criado_em DESC
        """
        try:
            self.db.cursor.execute(sql, (turma_id,))
            registros = self.db.cursor.fetchall()
            solicitacoes = []

            for registro in registros:
                solicitacoes.append(self.criar_solicitacao(registro))
            return solicitacoes

        except Exception as erro:
            print(f"Erro ao listar solicitações de compra por turma: {erro}")
            return []

    def atualizar_status(self, id_solicitacao, status):
        sql = """
            UPDATE solicitacoes_compras
            SET status = %s
            WHERE id_solicitacao = %s
        """
        try:
            self.db.cursor.execute(sql, (status, id_solicitacao))
            self.db.commit()

            if self.db.cursor.rowcount == 0:
                print("Solicitação não encontrada!")

            else:
                print("Status atualizado!")

        except Exception as erro:
            self.db.rollback()
            print(f"Erro ao atualizar status: {erro}")

    def excluir(self, id_solicitacao):
        sql = """
            DELETE FROM solicitacoes_compras
            WHERE id_solicitacao = %s
        """
        try:
            self.db.cursor.execute(sql, (id_solicitacao,))
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
