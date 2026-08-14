from database.conexao import Conexao
from models.log_auditoria import LogAuditoria

class LogAuditoriaRepository:
    """Somente leitura/inserção: log de auditoria não é editável nem excluível (RN-003)."""

    def __init__(self):
        self.db = Conexao()

    def criar_log(self, registro):
        return LogAuditoria(
            id_log=registro[0],
            usuario_id=registro[1],
            acao=registro[2],
            endereco_ip=registro[3],
            criado_em=registro[4]
        )

    def registrar(self, usuario_id, acao, endereco_ip = None):
        sql = """
        INSERT INTO logs_auditoria
        (
            usuario_id,
            acao,
            endereco_ip
        )
        VALUES
        (
            %s, %s, %s
        )
        """
        valores = (
            usuario_id,
            acao,
            endereco_ip
        )
        try:
            self.db.cursor.execute(sql, valores)
            self.db.commit()
            print("Log de auditoria registrado.")

        except Exception as erro:
            self.db.rollback()
            print(f"Erro ao registrar log de auditoria. Erro: {erro}")

    def buscar_por_id(self, id_log):
        sql = """
        SELECT *
        FROM logs_auditoria
        WHERE id = %s
        """
        try:
            self.db.cursor.execute(sql, (id_log,))
            registro = self.db.cursor.fetchone()

            if registro is None:
                return None

            return self.criar_log(registro)

        except Exception as erro:
            print(f"Erro ao buscar log de auditoria pelo id. Erro: {erro}")
            return None

    def listar(self):
        sql = """
            SELECT *
            FROM logs_auditoria
            ORDER BY criado_em DESC
        """
        try:
            self.db.cursor.execute(sql)
            registros = self.db.cursor.fetchall()
            logs = []

            for registro in registros:
                logs.append(self.criar_log(registro))
            return logs

        except Exception as erro:
            print(f"Erro ao listar logs de auditoria: {erro}")
            return []

    def listar_por_usuario(self, usuario_id):
        sql = """
            SELECT *
            FROM logs_auditoria
            WHERE usuario_id = %s
            ORDER BY criado_em DESC
        """
        try:
            self.db.cursor.execute(sql, (usuario_id,))
            registros = self.db.cursor.fetchall()
            logs = []

            for registro in registros:
                logs.append(self.criar_log(registro))
            return logs

        except Exception as erro:
            print(f"Erro ao listar logs de auditoria por usuário: {erro}")
            return []

    def fechar(self):
        self.db.fechar()
