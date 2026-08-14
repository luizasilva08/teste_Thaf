from utils.validacoes_gerais import validar_campo_obrigatorio

def validar_codigo_turma(codigo):
    validar_campo_obrigatorio(codigo, "código")
    return codigo.strip().upper()

def validar_periodo_turma(periodo):
    validar_campo_obrigatorio(periodo, "período")
    return periodo.strip()
