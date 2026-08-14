#class turma
class Turma:
    def __init__(self, id_turma = None,
                 codigo = "",
                 periodo = ""):

        self.id_turma = id_turma
        self.codigo = codigo
        self.periodo = periodo

    def __str__(self):
        c1  = "\033[38;5;22m"
        c2  = "\033[38;5;28m"
        c3  = "\033[38;5;34m"
        reset = "\033[0m"

        return (
            f"{c1}=== DADOS TURMA ==={reset}\n"
            f"{c2}Código:{reset} {self.codigo}\n"
            f"{c3}Período:{reset} {self.periodo}\n"
            f"{c1}=========================={reset}"
        )
