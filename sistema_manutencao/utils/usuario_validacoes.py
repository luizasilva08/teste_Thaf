import re

import bcrypt

from utils.validacoes_gerais import validar_campo_obrigatorio

REGEX_EMAIL = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def validar_nome_usuario(nome_usuario):
    validar_campo_obrigatorio(nome_usuario, "nome")
    return nome_usuario.strip()


def validar_email_usuario(email_usuario):
    validar_campo_obrigatorio(email_usuario, "e-mail")
    email_normalizado = email_usuario.strip().lower()

    if not REGEX_EMAIL.match(email_normalizado):
        raise ValueError(f"E-mail inválido: '{email_usuario}'.")
    return email_normalizado


def validar_senha_usuario(senha):
    validar_campo_obrigatorio(senha, "senha")
    if len(senha.strip()) < 6:
        raise ValueError("A senha deve ter pelo menos 6 caracteres.")
    return senha.strip()


def gerar_hash_senha(senha_texto_puro):
    hash_bytes = bcrypt.hashpw(senha_texto_puro.encode("utf-8"), bcrypt.gensalt())
    return hash_bytes.decode("utf-8")


def verificar_senha(senha_texto_puro, senha_hash):
    return bcrypt.checkpw(senha_texto_puro.encode("utf-8"), senha_hash.encode("utf-8"))
