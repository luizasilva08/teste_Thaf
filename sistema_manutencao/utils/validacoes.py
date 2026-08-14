import re

import bcrypt

from models.perfil import PERFIS_VALIDOS

REGEX_EMAIL = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


class ValidacaoError(Exception):
    pass


def validar_email(email: str) -> str:
    if not email or not REGEX_EMAIL.match(email):
        raise ValidacaoError(f"Email inválido: '{email}'.")
    return email.strip().lower()


def validar_nome_perfil(nome: str) -> str:
    if nome.lower() not in PERFIS_VALIDOS:
        raise ValidacaoError(f"Perfil inválido: '{nome}'. Válidos: {PERFIS_VALIDOS}.")
    return nome


def validar_campo_obrigatorio(valor, nome_campo: str):
    if valor is None or (isinstance(valor, str) and not valor.strip()):
        raise ValidacaoError(f"O campo '{nome_campo}' é obrigatório.")
    return valor


def validar_opcao(valor, opcoes_validas: tuple, nome_campo: str):
    if valor not in opcoes_validas:
        raise ValidacaoError(f"'{valor}' inválido para '{nome_campo}'. Válidos: {opcoes_validas}.")
    return valor


def gerar_hash_senha(senha_texto_puro: str) -> str:
    validar_campo_obrigatorio(senha_texto_puro, "senha")
    hash_bytes = bcrypt.hashpw(senha_texto_puro.encode("utf-8"), bcrypt.gensalt())
    return hash_bytes.decode("utf-8")


def verificar_senha(senha_texto_puro: str, senha_hash: str) -> bool:
    return bcrypt.checkpw(senha_texto_puro.encode("utf-8"), senha_hash.encode("utf-8"))


def exige_perfil(usuario_perfil_nome: str, perfis_permitidos: tuple):
    """Levanta PermissionError se o perfil do usuário não estiver entre os permitidos."""
    if usuario_perfil_nome.lower() not in [p.lower() for p in perfis_permitidos]:
        raise PermissionError(
            f"Ação restrita a {perfis_permitidos}. Perfil atual: '{usuario_perfil_nome}'."
        )
