#class usuario
class Usuario:
    def __init__(self, id_usuario = None,
                 perfil_id = None,
                 turma_id = None,
                 nome_usuario = "",
                 email_usuario = "",
                 senha_hash = "",
                 criado_em = None,
                 deleted_at = None):

        self.id_usuario = id_usuario
        self.perfil_id = perfil_id
        self.turma_id = turma_id
        self.nome_usuario = nome_usuario
        self.email_usuario = email_usuario
        self.senha_hash = senha_hash
        self.criado_em = criado_em
        self.deleted_at = deleted_at  # só é preenchido pelo módulo soft_delete/

    def __str__(self):
        c1  = "\033[38;5;53m"
        c2  = "\033[38;5;91m"
        c3  = "\033[38;5;135m"
        reset = "\033[0m"

        return (
            f"{c1}=== DADOS USUÁRIO ==={reset}\n"
            f"{c2}Nome:{reset} {self.nome_usuario}\n"
            f"{c3}E-mail:{reset} {self.email_usuario}\n"
            f"{c2}Perfil (id):{reset} {self.perfil_id}\n"
            f"{c3}Turma (id):{reset} {self.turma_id}\n"
            f"{c1}Criado em:{reset} {self.criado_em}\n"
            f"{c1}=========================={reset}"
        )
