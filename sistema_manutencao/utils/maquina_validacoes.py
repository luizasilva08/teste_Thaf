from models.maquina import STATUS_VALIDOS
from utils.validacoes_gerais import validar_campo_obrigatorio

def validar_tag_maquina(tag):
    validar_campo_obrigatorio(tag, "tag")
    return tag.strip().upper()

def validar_nome_maquina(nome):
    validar_campo_obrigatorio(nome, "nome")
    return nome.strip()

def validar_status_maquina(status_vivo):
    validar_campo_obrigatorio(status_vivo, "status")
    if status_vivo not in STATUS_VALIDOS:
        raise ValueError(
            f"Status inválido: '{status_vivo}'. Válidos: {', '.join(STATUS_VALIDOS)}."
        )
    return status_vivo
