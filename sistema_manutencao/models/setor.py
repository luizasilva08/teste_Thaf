#class setor
class Setor:
    def __init__(self, id_setor = None,
                 nome = "",
                 descricao = ""):

        self.id_setor = id_setor
        self.nome = nome
        self.descricao = descricao

    def __str__(self):
        c1  = "\033[38;5;24m"
        c2  = "\033[38;5;30m"
        c3  = "\033[38;5;37m"
        reset = "\033[0m"

        return (
            f"{c1}=== DADOS SETOR ==={reset}\n"
            f"{c2}Nome:{reset} {self.nome}\n"
            f"{c3}Descrição:{reset} {self.descricao}\n"
            f"{c1}=========================={reset}"
        )
