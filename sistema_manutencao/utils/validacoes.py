from models.perfil import PERFIS_VALIDOS

def validar_campo_obrigatorio(valor, nome_campo):
    if valor is None or not str(valor).strip():
        raise ValueError(f"O campo '{nome_campo}' é obrigatório.")
    return valor.strip()

def validar_nome_perfil(nome):
    validar_campo_obrigatorio(nome, "nome")
    nome_normalizado = nome.strip().upper()

    if nome_normalizado not in PERFIS_VALIDOS:
        raise ValueError(
            f"Perfil inválido: '{nome}'. Válidos: {', '.join(PERFIS_VALIDOS)}."
        )
    return nome_normalizado
