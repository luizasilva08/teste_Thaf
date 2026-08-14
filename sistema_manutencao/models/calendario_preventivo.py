FREQUENCIAS_VALIDAS = ("Diária", "Semanal", "Quinzenal", "Mensal", "Semestral", "Anual")
STATUS_VALIDOS = ("Agendada", "Em Execução", "Concluída", "Atrasada", "Cancelada")

DIAS_POR_FREQUENCIA = {
    "Diária": 1,
    "Semanal": 7,
    "Quinzenal": 15,
    "Mensal": 30,
    "Semestral": 182,
    "Anual": 365,
}

#class calendario_preventivo
class CalendarioPreventivo:
    def __init__(self, id_calendario = None,
                 maquina_id = None,
                 turma_id = None,
                 responsavel_id = None,
                 titulo_calendario = "",
                 descricao_calendario = None,
                 frequencia_calendario = "Mensal",
                 data_proxima_execucao = None,
                 status = "Agendada",
                 criado_em = None,
                 deleted_at = None):

        self.id_calendario = id_calendario
        self.maquina_id = maquina_id
        self.turma_id = turma_id
        self.responsavel_id = responsavel_id
        self.titulo_calendario = titulo_calendario
        self.descricao_calendario = descricao_calendario
        self.frequencia_calendario = frequencia_calendario
        self.data_proxima_execucao = data_proxima_execucao
        self.status = status
        self.criado_em = criado_em
        self.deleted_at = deleted_at  # só é preenchido pelo módulo soft_delete/

    def __str__(self):
        c1  = "\033[38;5;90m"
        c2  = "\033[38;5;133m"
        c3  = "\033[38;5;176m"
        reset = "\033[0m"

        return (
            f"{c1}=== CALENDÁRIO PREVENTIVO ==={reset}\n"
            f"{c2}Título:{reset} {self.titulo_calendario}\n"
            f"{c3}Máquina (id):{reset} {self.maquina_id}\n"
            f"{c2}Frequência:{reset} {self.frequencia_calendario}\n"
            f"{c3}Próxima execução:{reset} {self.data_proxima_execucao}\n"
            f"{c1}Status:{reset} {self.status}\n"
            f"{c1}=========================={reset}"
        )
