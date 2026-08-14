from database.conexao import obter_conexao
from models.maquina import Maquina
from repositories.base_repository import BaseRepository


class MaquinaRepository(BaseRepository):
    tabela = "maquinas"
    colunas = ("setor_id", "tag", "nome", "status_vivo")
    model_cls = Maquina

    def listar_por_setor(self, setor_id: int):
        return self.listar(filtros={"setor_id": setor_id})

    def listar_por_status(self, status: str):
        return self.listar(filtros={"status_vivo": status})

    def atualizar_status(self, id_: int, status_vivo: str) -> bool:
        sql = "UPDATE maquinas SET status_vivo = %s WHERE id = %s"
        conn = obter_conexao()
        try:
            cursor = conn.cursor()
            cursor.execute(sql, (status_vivo, id_))
            conn.commit()
            afetadas = cursor.rowcount
            cursor.close()
            return afetadas > 0
        finally:
            conn.close()

    def registrar_manutencao_concluida(self, id_: int) -> bool:
        sql = "UPDATE maquinas SET status_vivo = 'Operando', ultima_manutencao = NOW() WHERE id = %s"
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
