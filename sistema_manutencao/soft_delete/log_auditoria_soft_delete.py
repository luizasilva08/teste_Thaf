from database.conexao import Conexao
from models.log_auditoria import LogAuditoria

class LogAuditoriaSoftDelete:
    """Operações sobre logs de auditoria EXCLUÍDOS (ver notas em
    usuario_soft_delete.py). A PK aqui é só "id" (não "id_log"), única
    tabela do sistema que não recebeu prefixo.
    """

    def __init__(self):
        self.db = Conexao()

    def criar_log(self, registro):
        return LogAuditoria(
            id_log=registro[0],
            usuario_id=registro[1],
            acao=registro[2],
            endereco_ip=registro[3],
            criado_em=registro[4],
            deleted_at=registro[5]
        )

    def listar_excluidos(self):
        sql = """
            SELECT id, usuario_id, acao, endereco_ip, criado_em, deleted_at
            FROM logs_auditoria_deletados
            ORDER BY deleted_at DESC
        """
        try:
            self.db.cursor.execute(sql)
            registros = self.db.cursor.fetchall()
            logs = []

            for registro in registros:
                logs.append(self.criar_log(registro))
            return logs

        except Exception as erro:
            print(f"Erro ao listar logs excluídos: {erro}")
            return []

    def buscar_excluido_por_id(self, id_log):
        sql = """
            SELECT id, usuario_id, acao, endereco_ip, criado_em, deleted_at
            FROM logs_auditoria_deletados
            WHERE id = %s
        """
        try:
            self.db.cursor.execute(sql, (id_log,))
            registro = self.db.cursor.fetchone()

            if registro is None:
                return None

            return self.criar_log(registro)

        except Exception as erro:
            print(f"Erro ao buscar log excluído pelo id. Erro: {erro}")
            return None

    def restaurar(self, id_log):
        log = self.buscar_excluido_por_id(id_log)
        if log is None:
            print("Log excluído não encontrado!")
            return

        sql_inserir = """
            INSERT INTO logs_auditoria (id, usuario_id, acao, endereco_ip, criado_em)
            OVERRIDING SYSTEM VALUE
            VALUES (%s, %s, %s, %s, %s)
        """
        sql_apagar = """
            DELETE FROM logs_auditoria_deletados
            WHERE id = %s
        """
        try:
            self.db.cursor.execute(sql_inserir, (
                log.id_log, log.usuario_id, log.acao, log.endereco_ip, log.criado_em
            ))
            self.db.cursor.execute(sql_apagar, (id_log,))
            self.db.commit()
            print("Log restaurado com sucesso!")

        except Exception as erro:
            self.db.rollback()
            print(f"Erro ao restaurar log: {erro}")

    def fechar(self):
        self.db.fechar()
