TIPOS_MANUTENCAO_VALIDOS = ("Corretiva", "Preventiva", "Preditiva", "Melhoria")
CRITICIDADES_VALIDAS = ("Baixa", "Média", "Alta", "Crítica")

#class ordem_servico
class OrdemServico:
    def __init__(self, id_os = None,
                 solicitacao_id = None,
                 maquina_id = None,
                 turma_id = None,
                 tipo_manutencao = "Corretiva",
                 criticidade_os = "Média",
                 descricao_execucao = "",
                 pecas_usadas = None,
                 data_execucao = None,
                 hora_inicio = None,
                 hora_fim = None,
                 quantidade_pessoas = 1,
                 criado_em = None):

        self.id_os = id_os
        self.solicitacao_id = solicitacao_id
        self.maquina_id = maquina_id
        self.turma_id = turma_id
        self.tipo_manutencao = tipo_manutencao
        self.criticidade_os = criticidade_os
        self.descricao_execucao = descricao_execucao
        self.pecas_usadas = pecas_usadas
        self.data_execucao = data_execucao
        self.hora_inicio = hora_inicio
        self.hora_fim = hora_fim
        self.quantidade_pessoas = quantidade_pessoas
        self.criado_em = criado_em

    def __str__(self):
        c1  = "\033[38;5;94m"
        c2  = "\033[38;5;136m"
        c3  = "\033[38;5;179m"
        reset = "\033[0m"

        return (
            f"{c1}=== ORDEM DE SERVIÇO ==={reset}\n"
            f"{c2}Solicitação (id):{reset} {self.solicitacao_id}\n"
            f"{c3}Máquina (id):{reset} {self.maquina_id}\n"
            f"{c2}Tipo:{reset} {self.tipo_manutencao}\n"
            f"{c3}Criticidade:{reset} {self.criticidade_os}\n"
            f"{c1}Execução:{reset} {self.data_execucao} {self.hora_inicio}-{self.hora_fim}\n"
            f"{c1}=========================={reset}"
        )
