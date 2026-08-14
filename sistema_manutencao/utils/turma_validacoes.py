from utils.validacoes_gerais import validar_campo_obrigatorio

def validar_codigo_turma(codigo_turma):
    validar_campo_obrigatorio(codigo_turma, "código")
    return codigo_turma.strip().upper()

def validar_periodo_turma(periodo_turma):
    validar_campo_obrigatorio(periodo_turma, "período")
    return periodo_turma.strip()
