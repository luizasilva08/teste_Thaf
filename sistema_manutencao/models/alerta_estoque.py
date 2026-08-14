STATUS_ALERTA_VALIDOS = ("Pendente", "Resolvido")

#class alerta_estoque
class AlertaEstoque:
    def __init__(self, id_alerta = None,
                 item_id = None,
                 mensagem_alerta = "",
                 status = "Pendente",
                 criado_em = None):

        self.id_alerta = id_alerta
        self.item_id = item_id
        self.mensagem_alerta = mensagem_alerta
        self.status = status
        self.criado_em = criado_em

    def __str__(self):
        c1  = "\033[38;5;52m"
        c2  = "\033[38;5;168m"
        c3  = "\033[38;5;217m"
        reset = "\033[0m"

        return (
            f"{c1}=== ALERTA DE ESTOQUE ==={reset}\n"
            f"{c2}Item (id):{reset} {self.item_id}\n"
            f"{c3}Mensagem:{reset} {self.mensagem_alerta}\n"
            f"{c2}Status:{reset} {self.status}\n"
            f"{c1}=========================={reset}"
        )
