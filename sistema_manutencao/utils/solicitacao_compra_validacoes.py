from models.solicitacao_compra import STATUS_VALIDOS
from utils.validacoes_gerais import validar_campo_obrigatorio

def validar_especificacao_tecnica(especificacao_tecnica):
    validar_campo_obrigatorio(especificacao_tecnica, "especificação técnica")
    return especificacao_tecnica.strip()

def validar_justificativa(justificativa_solicitacao):
    validar_campo_obrigatorio(justificativa_solicitacao, "justificativa")
    return justificativa_solicitacao.strip()

def validar_status_compra(status):
    if status not in STATUS_VALIDOS:
        raise ValueError(f"Status inválido: '{status}'. Válidos: {', '.join(STATUS_VALIDOS)}.")
    return status
