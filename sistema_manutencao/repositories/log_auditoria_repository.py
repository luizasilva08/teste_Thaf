from database.conexao import obter_conexao
from models.log_auditoria import LogAuditoria


class LogAuditoriaRepository:
    """Somente leitura/inserção: log de auditoria não é editável nem excluível."""

    def registrar(self, usuario_id: int, acao: str, endereco_ip: str = None) -> int:
        sql = "INSERT INTO logs_auditoria (usuario_id, acao, endereco_ip) VALUES (%s, %s, %s)"
        conn = obter_conexao()
        try:
            cursor = conn.cursor()
            cursor.execute(sql, (usuario_id, acao, endereco_ip))
            conn.commit()
            novo_id = cursor.lastrowid
            cursor.close()
            return novo_id
        finally:
            conn.close()

    def listar_por_usuario(self, usuario_id: int):
        sql = "SELECT * FROM logs_auditoria WHERE usuario_id = %s ORDER BY criado_em DESC"
        conn = obter_conexao()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(sql, (usuario_id,))
            linhas = cursor.fetchall()
            cursor.close()
            return [LogAuditoria(**linha) for linha in linhas]
        finally:
            conn.close()
