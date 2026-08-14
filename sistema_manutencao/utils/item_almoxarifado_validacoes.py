from utils.validacoes_gerais import validar_campo_obrigatorio

def validar_nome_ferramenta(nome_ferramenta):
    validar_campo_obrigatorio(nome_ferramenta, "nome")
    return nome_ferramenta.strip()

def validar_quantidade(quantidade, nome_campo="quantidade"):
    if quantidade < 0:
        raise ValueError(f"O campo '{nome_campo}' não pode ser negativo.")
    return quantidade
