def validar_campo_obrigatorio(valor, nome_campo):
    if valor is None or not str(valor).strip():
        raise ValueError(f"O campo '{nome_campo}' é obrigatório.")
    return valor.strip()
