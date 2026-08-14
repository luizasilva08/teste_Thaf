"""Executa os scripts de database/tabelas/ para criar as tabelas no MySQL (Aiven).

As tabelas ficam em um arquivo por classe (database/tabelas/<numero>_<tabela>.sql)
para 13 pessoas trabalharem em paralelo sem conflitar no mesmo arquivo. O
prefixo numérico garante a ordem de criação (respeitando as FOREIGN KEY).
"""

import glob
import os

from database.conexao import Conexao

TABELAS_DIR = os.path.join(os.path.dirname(__file__), "tabelas")


def criar_tabelas():
    conexao = Conexao()

    arquivos = sorted(glob.glob(os.path.join(TABELAS_DIR, "*.sql")))

    try:
        for caminho in arquivos:
            with open(caminho, encoding="utf-8") as arquivo:
                script = arquivo.read()

            for comando in script.split(";"):
                comando = comando.strip()
                if comando:
                    conexao.cursor.execute(comando)

            print(f"OK: {os.path.basename(caminho)}")

        conexao.commit()
        print(f"Tabelas criadas com sucesso no banco '{conexao.database}'.")

    except Exception as erro:
        conexao.rollback()
        print(f"Erro ao criar tabelas: {erro}")

    finally:
        conexao.fechar()


if __name__ == "__main__":
    criar_tabelas()
