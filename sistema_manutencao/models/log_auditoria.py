#class log_auditoria
class LogAuditoria:
    def __init__(self, id_log = None,
                 usuario_id = None,
                 acao = "",
                 endereco_ip = None,
                 criado_em = None,
                 deleted_at = None):

        self.id_log = id_log
        self.usuario_id = usuario_id
        self.acao = acao
        self.endereco_ip = endereco_ip
        self.criado_em = criado_em
        self.deleted_at = deleted_at  # só é preenchido pelo módulo soft_delete/

    def __str__(self):
        c1  = "\033[38;5;236m"
        c2  = "\033[38;5;244m"
        c3  = "\033[38;5;252m"
        reset = "\033[0m"

        return (
            f"{c1}=== LOG DE AUDITORIA ==={reset}\n"
            f"{c2}Usuário (id):{reset} {self.usuario_id}\n"
            f"{c3}Ação:{reset} {self.acao}\n"
            f"{c2}IP:{reset} {self.endereco_ip}\n"
            f"{c3}Data/hora:{reset} {self.criado_em}\n"
            f"{c1}=========================={reset}"
        )
