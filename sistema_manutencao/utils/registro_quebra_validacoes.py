from utils.validacoes_gerais import validar_campo_obrigatorio

def validar_descricao_quebra(descricao_quebra):
    validar_campo_obrigatorio(descricao_quebra, "descrição")
    return descricao_quebra.strip()
