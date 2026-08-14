from utils.validacoes_gerais import validar_campo_obrigatorio

def validar_nome_setor(nome):
    validar_campo_obrigatorio(nome, "nome")
    return nome.strip()
