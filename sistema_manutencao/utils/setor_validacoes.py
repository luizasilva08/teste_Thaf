from utils.validacoes_gerais import validar_campo_obrigatorio

def validar_nome_setor(nome_setor):
    validar_campo_obrigatorio(nome_setor, "nome")
    return nome_setor.strip()
