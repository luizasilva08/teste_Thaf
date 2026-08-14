from utils.validacoes_gerais import validar_campo_obrigatorio

def validar_acao(acao):
    validar_campo_obrigatorio(acao, "ação")
    return acao.strip()
