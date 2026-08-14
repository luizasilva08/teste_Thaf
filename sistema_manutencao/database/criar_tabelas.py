"""Executa o schema.sql para criar o banco ctw_manutencao e suas tabelas."""

import os

import mysql.connector

from database.conexao import _config

SCHEMA_PATH = os.path.join(os.path.dirname(__file__), "schema.sql")


def criar_tabelas():
    config = _config()
    database = config.pop("database")

    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()

    with open(SCHEMA_PATH, encoding="utf-8") as arquivo:
        script = arquivo.read()

    for comando in script.split(";"):
        comando = comando.strip()
        if comando:
            cursor.execute(comando)

    conn.commit()
    cursor.close()
    conn.close()
    print(f"Banco '{database}' e tabelas criados com sucesso.")


if __name__ == "__main__":
    criar_tabelas()
