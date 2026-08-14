"""Executa o database/schema.sql para criar as tabelas no MySQL (Aiven)."""

import os

from database.conexao import Conexao

SCHEMA_PATH = os.path.join(os.path.dirname(__file__), "schema.sql")


def criar_tabelas():
    conexao = Conexao()

    with open(SCHEMA_PATH, encoding="utf-8") as arquivo:
        script = arquivo.read()

    try:
        for comando in script.split(";"):
            comando = comando.strip()
            if comando:
                conexao.cursor.execute(comando)

        conexao.commit()
        print(f"Tabelas criadas com sucesso no banco '{conexao.database}'.")

    except Exception as erro:
        conexao.rollback()
        print(f"Erro ao criar tabelas: {erro}")

    finally:
        conexao.fechar()


if __name__ == "__main__":
    criar_tabelas()
