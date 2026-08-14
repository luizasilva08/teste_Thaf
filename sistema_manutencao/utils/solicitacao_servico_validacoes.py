from models.solicitacao_servico import PRIORIDADES_VALIDAS, TIPOS_MANUTENCAO_VALIDOS
from utils.validacoes_gerais import validar_campo_obrigatorio

def validar_descricao_problema(descricao_problema):
    validar_campo_obrigatorio(descricao_problema, "descrição do problema")
    return descricao_problema.strip()

def validar_prioridade_ss(prioridade_ss):
    if prioridade_ss not in PRIORIDADES_VALIDAS:
        raise ValueError(f"Prioridade inválida: '{prioridade_ss}'. Válidas: {', '.join(PRIORIDADES_VALIDAS)}.")
    return prioridade_ss

def validar_tipo_manutencao_ss(tipo_manutencao):
    if tipo_manutencao not in TIPOS_MANUTENCAO_VALIDOS:
        raise ValueError(f"Tipo inválido: '{tipo_manutencao}'. Válidos: {', '.join(TIPOS_MANUTENCAO_VALIDOS)}.")
    return tipo_manutencao
