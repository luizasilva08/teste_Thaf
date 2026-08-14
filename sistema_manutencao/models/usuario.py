#class usuario
class Usuario:
    def __init__(self, id_usuario = None,
                 perfil_id = None,
                 turma_id = None,
                 nome = "",
                 email = "",
                 senha_hash = "",
                 criado_em = None):

        self.id_usuario = id_usuario
        self.perfil_id = perfil_id
        self.turma_id = turma_id
        self.nome = nome
        self.email = email
        self.senha_hash = senha_hash
        self.criado_em = criado_em

    def __str__(self):
        c1  = "\033[38;5;53m"
        c2  = "\033[38;5;91m"
        c3  = "\033[38;5;135m"
        reset = "\033[0m"

        return (
            f"{c1}=== DADOS USUÁRIO ==={reset}\n"
            f"{c2}Nome:{reset} {self.nome}\n"
            f"{c3}E-mail:{reset} {self.email}\n"
            f"{c2}Perfil (id):{reset} {self.perfil_id}\n"
            f"{c3}Turma (id):{reset} {self.turma_id}\n"
            f"{c1}Criado em:{reset} {self.criado_em}\n"
            f"{c1}=========================={reset}"
        )
