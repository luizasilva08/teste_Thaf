from datetime import date, timedelta

from database.conexao import obter_conexao
from models.calendario_preventivo import DIAS_POR_FREQUENCIA, CalendarioPreventivo
from repositories.base_repository import BaseRepository


class CalendarioPreventivoRepository(BaseRepository):
    tabela = "calendario_preventivo"
    colunas = (
        "maquina_id",
        "turma_id",
        "responsavel_id",
        "titulo",
        "descricao",
        "frequencia",
        "data_proxima_execucao",
        "status",
    )
    model_cls = CalendarioPreventivo

    def listar_por_periodo(self, data_inicio: date, data_fim: date):
        sql = (
            "SELECT * FROM calendario_preventivo "
            "WHERE data_proxima_execucao BETWEEN %s AND %s "
            "ORDER BY data_proxima_execucao"
        )
        conn = obter_conexao()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(sql, (data_inicio, data_fim))
            linhas = cursor.fetchall()
            cursor.close()
            return [self._linha_para_model(linha) for linha in linhas]
        finally:
            conn.close()

    def listar_atrasadas(self):
        sql = (
            "SELECT * FROM calendario_preventivo "
            "WHERE data_proxima_execucao < %s AND status = 'Agendada' "
            "ORDER BY data_proxima_execucao"
        )
        conn = obter_conexao()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(sql, (date.today(),))
            linhas = cursor.fetchall()
            cursor.close()
            return [self._linha_para_model(linha) for linha in linhas]
        finally:
            conn.close()

    def marcar_atrasadas(self) -> int:
        sql = (
            "UPDATE calendario_preventivo SET status = 'Atrasada' "
            "WHERE data_proxima_execucao < %s AND status = 'Agendada'"
        )
        conn = obter_conexao()
        try:
            cursor = conn.cursor()
            cursor.execute(sql, (date.today(),))
            conn.commit()
            afetadas = cursor.rowcount
            cursor.close()
            return afetadas
        finally:
            conn.close()

    def marcar_concluida(self, id_: int) -> CalendarioPreventivo:
        """Conclui a ocorrência atual e agenda a próxima automaticamente."""
        atual = self.buscar_por_id(id_)
        if atual is None:
            raise ValueError(f"Item de calendário {id_} não encontrado.")

        conn = obter_conexao()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE calendario_preventivo SET status = 'Concluída' WHERE id = %s",
                (id_,),
            )
            conn.commit()
            cursor.close()
        finally:
            conn.close()

        dias = DIAS_POR_FREQUENCIA[atual.frequencia]
        proxima = CalendarioPreventivo(
            maquina_id=atual.maquina_id,
            turma_id=atual.turma_id,
            responsavel_id=atual.responsavel_id,
            titulo=atual.titulo,
            descricao=atual.descricao,
            frequencia=atual.frequencia,
            data_proxima_execucao=atual.data_proxima_execucao + timedelta(days=dias),
            status="Agendada",
        )
        self.criar(proxima)
        return self.buscar_por_id(id_)
