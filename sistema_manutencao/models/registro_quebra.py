#class registro_quebra
class RegistroQuebra:
    def __init__(self, id_quebra = None,
                 item_id = None,
                 usuario_id = None,
                 descricao_quebra = "",
                 foto_url = None,
                 criado_em = None,
                 deleted_at = None):

        self.id_quebra = id_quebra
        self.item_id = item_id
        self.usuario_id = usuario_id
        self.descricao_quebra = descricao_quebra
        self.foto_url = foto_url
        self.criado_em = criado_em
        self.deleted_at = deleted_at  # só é preenchido pelo módulo soft_delete/

    def __str__(self):
        c1  = "\033[38;5;240m"
        c2  = "\033[38;5;250m"
        c3  = "\033[38;5;255m"
        reset = "\033[0m"

        return (
            f"{c1}=== REGISTRO DE QUEBRA ==={reset}\n"
            f"{c2}Item (id):{reset} {self.item_id}\n"
            f"{c3}Usuário (id):{reset} {self.usuario_id}\n"
            f"{c2}Descrição:{reset} {self.descricao_quebra}\n"
            f"{c3}Foto:{reset} {self.foto_url}\n"
            f"{c1}=========================={reset}"
        )
