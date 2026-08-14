from models.maquina import STATUS_VALIDOS
from utils.validacoes_gerais import validar_campo_obrigatorio

def validar_tag_maquina(tag_maquina):
    validar_campo_obrigatorio(tag_maquina, "tag")
    return tag_maquina.strip().upper()

def validar_nome_maquina(nome_maquina):
    validar_campo_obrigatorio(nome_maquina, "nome")
    return nome_maquina.strip()

def validar_status_maquina(status_vivo):
    validar_campo_obrigatorio(status_vivo, "status")
    if status_vivo not in STATUS_VALIDOS:
        raise ValueError(
            f"Status inválido: '{status_vivo}'. Válidos: {', '.join(STATUS_VALIDOS)}."
        )
    return status_vivo
