from datetime import datetime

from models.calendario_preventivo import FREQUENCIAS_VALIDAS
from utils.validacoes_gerais import validar_campo_obrigatorio

def validar_titulo_calendario(titulo_calendario):
    validar_campo_obrigatorio(titulo_calendario, "título")
    return titulo_calendario.strip()

def validar_frequencia(frequencia_calendario):
    if frequencia_calendario not in FREQUENCIAS_VALIDAS:
        raise ValueError(f"Frequência inválida: '{frequencia_calendario}'. Válidas: {', '.join(FREQUENCIAS_VALIDAS)}.")
    return frequencia_calendario

def validar_data_execucao(texto_data):
    validar_campo_obrigatorio(texto_data, "data de execução")
    try:
        return datetime.strptime(texto_data.strip(), "%Y-%m-%d").date()
    except ValueError:
        raise ValueError("Data inválida. Use o formato AAAA-MM-DD.")
