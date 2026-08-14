from utils.validacoes_gerais import validar_campo_obrigatorio

def validar_mensagem_alerta(mensagem_alerta):
    validar_campo_obrigatorio(mensagem_alerta, "mensagem")
    return mensagem_alerta.strip()
