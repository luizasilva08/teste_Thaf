"""Executa os scripts de database/tabelas/ para criar o schema no PostgreSQL (Aiven).

As tabelas ficam em um arquivo por classe (database/tabelas/<numero>_<tabela>.sql)
para 13 pessoas trabalharem em paralelo sem conflitar no mesmo arquivo. O
prefixo numérico garante a ordem de execução: 00_ = tipos/funções
compartilhadas (rodam antes de tudo), depois uma tabela por número,
respeitando as FOREIGN KEY.

Cada arquivo é enviado ao banco de uma vez só (sem dividir por ";" no
Python) porque as funções em PL/pgSQL (00_funcoes.sql) têm ponto e vírgula
dentro do corpo "$$ ... $$" — dividir a string quebraria essas funções.
O PostgreSQL já sabe executar vários comandos separados por ";" em uma
única chamada.
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

            conexao.cursor.execute(script)
            print(f"OK: {os.path.basename(caminho)}")

        conexao.commit()
        print(f"Schema criado com sucesso no banco '{conexao.database}'.")

    except Exception as erro:
        conexao.rollback()
        print(f"Erro ao criar schema: {erro}")

    finally:
        conexao.fechar()


if __name__ == "__main__":
    criar_tabelas()
