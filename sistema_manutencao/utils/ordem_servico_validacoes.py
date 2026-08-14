from datetime import datetime

from models.ordem_servico import CRITICIDADES_VALIDAS, TIPOS_MANUTENCAO_VALIDOS
from utils.validacoes_gerais import validar_campo_obrigatorio

def validar_descricao_execucao(descricao_execucao):
    validar_campo_obrigatorio(descricao_execucao, "descrição da execução")
    return descricao_execucao.strip()

def validar_tipo_manutencao_os(tipo_manutencao):
    if tipo_manutencao not in TIPOS_MANUTENCAO_VALIDOS:
        raise ValueError(f"Tipo inválido: '{tipo_manutencao}'. Válidos: {', '.join(TIPOS_MANUTENCAO_VALIDOS)}.")
    return tipo_manutencao

def validar_criticidade_os(criticidade_os):
    if criticidade_os not in CRITICIDADES_VALIDAS:
        raise ValueError(f"Criticidade inválida: '{criticidade_os}'. Válidas: {', '.join(CRITICIDADES_VALIDAS)}.")
    return criticidade_os

def validar_data(texto_data):
    validar_campo_obrigatorio(texto_data, "data")
    try:
        return datetime.strptime(texto_data.strip(), "%Y-%m-%d").date()
    except ValueError:
        raise ValueError("Data inválida. Use o formato AAAA-MM-DD.")

def validar_hora(texto_hora, nome_campo="hora"):
    validar_campo_obrigatorio(texto_hora, nome_campo)
    try:
        return datetime.strptime(texto_hora.strip(), "%H:%M").time()
    except ValueError:
        raise ValueError(f"'{nome_campo}' inválida. Use o formato HH:MM.")
