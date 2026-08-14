STATUS_VALIDOS = ("Operando", "Manutenção", "Parado", "Crítico")

#class maquina
class Maquina:
    def __init__(self, id_maquina = None,
                 setor_id = None,
                 tag_maquina = "",
                 nome_maquina = "",
                 status_vivo = "Operando",
                 ultima_manutencao = None):

        self.id_maquina = id_maquina
        self.setor_id = setor_id
        self.tag_maquina = tag_maquina
        self.nome_maquina = nome_maquina
        self.status_vivo = status_vivo
        self.ultima_manutencao = ultima_manutencao

    def __str__(self):
        c1  = "\033[38;5;24m"
        c2  = "\033[38;5;30m"
        c3  = "\033[38;5;37m"
        reset = "\033[0m"

        return (
            f"{c1}=== DADOS MÁQUINA ==={reset}\n"
            f"{c2}Tag:{reset} {self.tag_maquina}\n"
            f"{c3}Nome:{reset} {self.nome_maquina}\n"
            f"{c2}Setor (id):{reset} {self.setor_id}\n"
            f"{c3}Status:{reset} {self.status_vivo}\n"
            f"{c1}Última manutenção:{reset} {self.ultima_manutencao}\n"
            f"{c1}=========================={reset}"
        )
