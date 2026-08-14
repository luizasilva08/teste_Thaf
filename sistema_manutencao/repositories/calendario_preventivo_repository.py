from datetime import date, timedelta

from database.conexao import Conexao
from models.calendario_preventivo import DIAS_POR_FREQUENCIA, CalendarioPreventivo

class CalendarioPreventivoRepository:
    """calendario_preventivo usa soft delete por HERANÇA (ver notas em
    usuario_repository.py) — usa "FROM ONLY calendario_preventivo".
    """

    def __init__(self):
        self.db = Conexao()

    def criar_calendario(self, registro):
        return CalendarioPreventivo(
            id_calendario=registro[0],
            maquina_id=registro[1],
            turma_id=registro[2],
            responsavel_id=registro[3],
            titulo_calendario=registro[4],
            descricao_calendario=registro[5],
            frequencia_calendario=registro[6],
            data_proxima_execucao=registro[7],
            status=registro[8],
            criado_em=registro[9]
        )

    def salvar(self, calendario):
        sql = """
        INSERT INTO calendario_preventivo
        (
            maquina_id,
            turma_id,
            responsavel_id,
            titulo_calendario,
            descricao_calendario,
            frequencia_calendario,
            data_proxima_execucao
        )
        VALUES
        (
            %s, %s, %s, %s, %s, %s, %s
        )
        """
        valores = (
            calendario.maquina_id,
            calendario.turma_id,
            calendario.responsavel_id,
            calendario.titulo_calendario,
            calendario.descricao_calendario,
            calendario.frequencia_calendario,
            calendario.data_proxima_execucao
        )
        try:
            self.db.cursor.execute(sql, valores)
            self.db.commit()
            print("Agendamento cadastrado com sucesso!")

        except Exception as erro:
            self.db.rollback()
            print(f"Erro ao cadastrar agendamento. Erro: {erro}")

    def buscar_por_id(self, id_calendario):
        sql = """
        SELECT id_calendario, maquina_id, turma_id, responsavel_id, titulo_calendario,
               descricao_calendario, frequencia_calendario, data_proxima_execucao, status, criado_em
        FROM ONLY calendario_preventivo
        WHERE id_calendario = %s
        """
        try:
            self.db.cursor.execute(sql, (id_calendario,))
            registro = self.db.cursor.fetchone()

            if registro is None:
                return None

            return self.criar_calendario(registro)

        except Exception as erro:
            print(f"Erro ao buscar agendamento pelo id. Erro: {erro}")
            return None

    def listar(self):
        sql = """
            SELECT id_calendario, maquina_id, turma_id, responsavel_id, titulo_calendario,
                   descricao_calendario, frequencia_calendario, data_proxima_execucao, status, criado_em
            FROM ONLY calendario_preventivo
            ORDER BY data_proxima_execucao
        """
        try:
            self.db.cursor.execute(sql)
            registros = self.db.cursor.fetchall()
            calendarios = []

            for registro in registros:
                calendarios.append(self.criar_calendario(registro))
            return calendarios

        except Exception as erro:
            print(f"Erro ao listar agendamentos: {erro}")
            return []

    def listar_por_periodo(self, data_inicio, data_fim):
        sql = """
            SELECT id_calendario, maquina_id, turma_id, responsavel_id, titulo_calendario,
                   descricao_calendario, frequencia_calendario, data_proxima_execucao, status, criado_em
            FROM ONLY calendario_preventivo
            WHERE data_proxima_execucao BETWEEN %s AND %s
            ORDER BY data_proxima_execucao
        """
        try:
            self.db.cursor.execute(sql, (data_inicio, data_fim))
            registros = self.db.cursor.fetchall()
            calendarios = []

            for registro in registros:
                calendarios.append(self.criar_calendario(registro))
            return calendarios

        except Exception as erro:
            print(f"Erro ao listar agendamentos por período: {erro}")
            return []

    def listar_atrasadas(self):
        sql = """
            SELECT id_calendario, maquina_id, turma_id, responsavel_id, titulo_calendario,
                   descricao_calendario, frequencia_calendario, data_proxima_execucao, status, criado_em
            FROM ONLY calendario_preventivo
            WHERE data_proxima_execucao < %s AND status = 'Agendada'
            ORDER BY data_proxima_execucao
        """
        try:
            self.db.cursor.execute(sql, (date.today(),))
            registros = self.db.cursor.fetchall()
            calendarios = []

            for registro in registros:
                calendarios.append(self.criar_calendario(registro))
            return calendarios

        except Exception as erro:
            print(f"Erro ao listar agendamentos atrasados: {erro}")
            return []

    def marcar_atrasadas(self):
        sql = """
            UPDATE calendario_preventivo
            SET status = 'Atrasada'
            WHERE data_proxima_execucao < %s AND status = 'Agendada'
        """
        try:
            self.db.cursor.execute(sql, (date.today(),))
            self.db.commit()
            return self.db.cursor.rowcount

        except Exception as erro:
            self.db.rollback()
            print(f"Erro ao marcar agendamentos atrasados: {erro}")
            return 0

    def marcar_concluida(self, id_calendario):
        """Conclui a ocorrência atual e agenda a próxima automaticamente."""
        atual = self.buscar_por_id(id_calendario)
        if atual is None:
            print("Agendamento não encontrado!")
            return

        sql = """
            UPDATE calendario_preventivo
            SET status = 'Concluída'
            WHERE id_calendario = %s
        """
        try:
            self.db.cursor.execute(sql, (id_calendario,))
            self.db.commit()

        except Exception as erro:
            self.db.rollback()
            print(f"Erro ao concluir agendamento: {erro}")
            return

        dias = DIAS_POR_FREQUENCIA[atual.frequencia_calendario]
        proxima = CalendarioPreventivo(
            maquina_id=atual.maquina_id,
            turma_id=atual.turma_id,
            responsavel_id=atual.responsavel_id,
            titulo_calendario=atual.titulo_calendario,
            descricao_calendario=atual.descricao_calendario,
            frequencia_calendario=atual.frequencia_calendario,
            data_proxima_execucao=atual.data_proxima_execucao + timedelta(days=dias)
        )
        self.salvar(proxima)
        print("Agendamento concluído — próxima ocorrência já criada.")

    def excluir(self, id_calendario):
        sql = """
            DELETE FROM calendario_preventivo
            WHERE id_calendario = %s
        """
        try:
            self.db.cursor.execute(sql, (id_calendario,))
            self.db.commit()

            if self.db.cursor.rowcount == 0:
                print("Agendamento não encontrado!")

            else:
                print("Agendamento excluído com sucesso!")

        except Exception as erro:
            self.db.rollback()
            print(f"Erro ao excluir agendamento: {erro}")

    def fechar(self):
        self.db.fechar()
