# Passo a passo da classe Perfil — código pronto para copiar e colar

Esses são os códigos reais já implementados no repositório (pasta
`sistema_manutencao/`). Sirva-se deles como modelo: para criar a próxima
classe (Usuario, Ativo, OrdemServico...), copie cada bloco, cole no arquivo
correspondente da nova pasta/arquivo e troque "Perfil"/"perfis" pelo nome da
nova classe/tabela.

**Tabela SQL:** `perfis`
**Classe:** `Perfil`
**Comando do Git:**
```
git checkout -b "Feature/Issue-#1/Perfis"
```

---

## 1. `database/tabelas/01_perfis.sql`

Cada tabela é um arquivo próprio dentro de `database/tabelas/`, com um
**prefixo numérico** que garante a ordem de criação (uma tabela com FK
precisa nascer depois da tabela que ela referencia). Perfis é `01_` porque
nada depende dela; a próxima classe pega o próximo número livre.

```sql
CREATE TABLE perfis (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(50) NOT NULL UNIQUE,
    descricao TEXT,
    CONSTRAINT chk_perfil_nome CHECK (
        LOWER(nome) IN ('coordenador', 'gestor', 'professor', 'aluno', 'representante')
    )
);
```

## 2. `models/perfil.py`

```python
PERFIS_VALIDOS = ("coordenador", "gestor", "professor", "aluno", "representante")

#class perfil
class Perfil:
    def __init__(self, id_perfil = None,
                 nome = "",
                 descricao = ""):

        self.id_perfil = id_perfil
        self.nome = nome
        self.descricao = descricao

    def __str__(self):
        c1  = "\033[38;5;17m"
        c2  = "\033[38;5;18m"
        c3  = "\033[38;5;19m"
        reset = "\033[0m"

        return (
            f"{c1}=== DADOS PERFIL ==={reset}\n"
            f"{c2}Nome:{reset} {self.nome}\n"
            f"{c3}Descrição:{reset} {self.descricao}\n"
            f"{c1}=========================={reset}"
        )
```

## 3. `repositories/perfil_repository.py`

```python
from database.conexao import Conexao
from models.perfil import Perfil

class PerfilRepository:
    def __init__(self):
        self.db = Conexao()

    def criar_perfil(self, registro):
        return Perfil(
            id_perfil=registro[0],
            nome=registro[1],
            descricao=registro[2]
        )

    def salvar(self, perfil):
        sql = """
        INSERT INTO perfis
        (
            nome,
            descricao
        )
        VALUES
        (
            %s, %s
        )
        """
        valores = (
            perfil.nome,
            perfil.descricao
        )
        try:
            self.db.cursor.execute(sql, valores)
            self.db.commit()
            print("Perfil cadastrado com sucesso!")

        except Exception as erro:
            self.db.rollback()
            print(f"Erro ao cadastrar perfil. Erro: {erro}")

    def buscar_por_id(self, id_perfil):
        sql = """
        SELECT *
        FROM perfis
        WHERE id = %s
        """
        try:
            self.db.cursor.execute(sql, (id_perfil,))
            registro = self.db.cursor.fetchone()

            if registro is None:
                return None

            return self.criar_perfil(registro)

        except Exception as erro:
            print(f"Erro ao buscar perfil pelo id. Erro: {erro}")
            return None

    def listar(self):
        sql = """
            SELECT *
            FROM perfis
            ORDER BY nome
        """
        try:
            self.db.cursor.execute(sql)
            registros = self.db.cursor.fetchall()
            perfis = []

            for registro in registros:
                perfis.append(self.criar_perfil(registro))
            return perfis

        except Exception as erro:
            print(f"Erro ao listar perfis: {erro}")
            return []

    def atualizar(self, perfil):
        sql = """UPDATE perfis
        SET
            nome = %s,
            descricao = %s
        WHERE id = %s
        """
        valores = (
            perfil.nome,
            perfil.descricao,
            perfil.id_perfil
        )
        try:
            self.db.cursor.execute(sql, valores)
            self.db.commit()
            if self.db.cursor.rowcount == 0:
                print("Perfil não encontrado!")

            else:
                print("Perfil atualizado!")

        except Exception as erro:
            self.db.rollback()
            print(f"Erro ao atualizar perfil: {erro}")

    def excluir(self, id_perfil):
        sql = """
            DELETE FROM perfis
            WHERE id = %s
        """
        try:
            self.db.cursor.execute(sql, (id_perfil,))
            self.db.commit()

            if self.db.cursor.rowcount == 0:
                print("Perfil não encontrado!")

            else:
                print("Perfil excluído com sucesso!")

        except Exception as erro:
            self.db.rollback()
            print(f"Erro ao excluir perfil: {erro}")

    def fechar(self):
        self.db.fechar()
```

## 4. `utils/` — validações

Pra 13 pessoas não esbarrarem no mesmo arquivo, as validações são separadas
em **um arquivo por classe** + um arquivo **genérico compartilhado**. Quando
for criar a próxima classe, **não edite `perfil_validacoes.py`** — crie
`utils/<sua_classe>_validacoes.py` do zero, seguindo este modelo.

**`utils/validacoes_gerais.py`** (compartilhado — só mexa aqui se for criar
uma validação realmente genérica, nova, adicionada no final do arquivo):

```python
def validar_campo_obrigatorio(valor, nome_campo):
    if valor is None or not str(valor).strip():
        raise ValueError(f"O campo '{nome_campo}' é obrigatório.")
    return valor.strip()
```

**`utils/perfil_validacoes.py`** (específico da classe Perfil):

```python
from models.perfil import PERFIS_VALIDOS
from utils.validacoes_gerais import validar_campo_obrigatorio

def validar_nome_perfil(nome):
    validar_campo_obrigatorio(nome, "nome")
    nome_normalizado = nome.strip().lower()

    if nome_normalizado not in PERFIS_VALIDOS:
        raise ValueError(
            f"Perfil inválido: '{nome}'. Válidos: {', '.join(PERFIS_VALIDOS)}."
        )
    return nome_normalizado
```

## 5. `menus/` — menu principal + um submenu por classe

Pra 13 pessoas não conflitarem no menu, ele virou uma pasta: um arquivo
compartilhado com o texto em gradiente, um `menu_principal.py` pequeno (só
lista os módulos) e **um arquivo por classe** com o submenu completo. Ao
criar uma nova classe, você cria `menus/<sua_classe>_menu.py` do zero e só
adiciona **2 linhas** em `menus/menu_principal.py` (import + opção).

**`menus/gradiente.py`** (compartilhado, praticamente nunca muda):

```python
def gradiente_texto(texto, cor_inicio, cor_fim):
    """Aplica um gradiente de cor a uma linha de texto usando ANSI truecolor."""
    r1, g1, b1 = cor_inicio
    r2, g2, b2 = cor_fim
    tamanho = len(texto)
    resultado = ""
    for i, char in enumerate(texto):
        if tamanho <= 1:
            t = 0
        else:
            t = i / (tamanho - 1)
        r = int(r1 + (r2 - r1) * t)
        g = int(g1 + (g2 - g1) * t)
        b = int(b1 + (b2 - b1) * t)
        resultado += f"\033[38;2;{r};{g};{b}m{char}"
    resultado += "\033[0m"
    return resultado
```

**`menus/menu_principal.py`** (o único arquivo compartilhado de verdade — a
lista de imports e a lista de opções crescem, mas o resto não muda):

```python
from menus.gradiente import gradiente_texto
from menus.perfil_menu import MenuPerfil


class MenuPrincipal:

    # Azul institucional: azul-marinho -> azul de aço -> azul claro
    AZUL_MARINHO = (10, 30, 60)
    AZUL_ACO = (40, 90, 160)
    AZUL_CLARO = (150, 195, 235)

    def exibir(self):
        while True:
            print()
            print(gradiente_texto("=" * 60, self.AZUL_MARINHO, self.AZUL_CLARO))
            print(gradiente_texto("CTW MANUTENÇÃO - MENU PRINCIPAL", self.AZUL_ACO, self.AZUL_CLARO))
            print(gradiente_texto("=" * 60, self.AZUL_CLARO, self.AZUL_MARINHO))
            print(gradiente_texto("1 - Perfis", self.AZUL_MARINHO, self.AZUL_ACO))
            print(gradiente_texto("0 - Sair", self.AZUL_MARINHO, self.AZUL_ACO))
            print(gradiente_texto("=" * 60, self.AZUL_CLARO, self.AZUL_MARINHO))

            opcao = input(gradiente_texto("Escolha uma opção: ", self.AZUL_CLARO, self.AZUL_MARINHO))

            if opcao == "1":
                MenuPerfil().exibir()

            elif opcao == "0":
                print()
                print(gradiente_texto("Sistema Encerrado", self.AZUL_MARINHO, self.AZUL_ACO))
                break

            else:
                print()
                print(gradiente_texto("Opção inválida!", self.AZUL_CLARO, self.AZUL_MARINHO))
```

**`menus/perfil_menu.py`** (exemplo completo — submenu de uma classe):

```python
from models.perfil import Perfil
from repositories.perfil_repository import PerfilRepository
from utils.perfil_validacoes import validar_nome_perfil

from menus.gradiente import gradiente_texto


class MenuPerfil:

    # Laranja segurança: aço escuro -> laranja industrial -> âmbar claro
    ACO_ESCURO = (30, 34, 40)
    LARANJA = (217, 98, 43)
    AMBAR = (240, 180, 110)

    def __init__(self):
        self.repository = PerfilRepository()

    # submenu
    def exibir(self):
        while True:
            print()
            print(gradiente_texto("=" * 60, self.ACO_ESCURO, self.AMBAR))
            print(gradiente_texto("CTW MANUTENÇÃO - PERFIS DE ACESSO", self.LARANJA, self.AMBAR))
            print(gradiente_texto("=" * 60, self.AMBAR, self.ACO_ESCURO))
            print(gradiente_texto("1 - Cadastrar Perfil", self.ACO_ESCURO, self.LARANJA))
            print(gradiente_texto("2 - Buscar Perfil", self.ACO_ESCURO, self.LARANJA))
            print(gradiente_texto("3 - Listar Perfis", self.LARANJA, self.AMBAR))
            print(gradiente_texto("4 - Atualizar Perfil", self.LARANJA, self.AMBAR))
            print(gradiente_texto("5 - Excluir Perfil", self.ACO_ESCURO, self.AMBAR))
            print(gradiente_texto("0 - Sair", self.ACO_ESCURO, self.LARANJA))
            print(gradiente_texto("=" * 60, self.AMBAR, self.ACO_ESCURO))

            opcao = input(gradiente_texto("Escolha uma opção: ", self.AMBAR, self.ACO_ESCURO))

            if opcao == "1":
                self.cadastrar_perfil()

            elif opcao == "2":
                self.buscar_perfil()

            elif opcao == "3":
                self.listar_perfil()

            elif opcao == "4":
                self.atualizar_perfil()

            elif opcao == "5":
                self.excluir_perfil()

            elif opcao == "0":
                self.repository.fechar()
                print()
                print(gradiente_texto("Voltando ao menu principal...", self.ACO_ESCURO, self.LARANJA))
                break

            else:
                print()
                print(gradiente_texto("Opção inválida!", self.AMBAR, self.ACO_ESCURO))

    def cadastrar_perfil(self):
        print()
        print(gradiente_texto("=" * 60, self.ACO_ESCURO, self.AMBAR))
        print(gradiente_texto("CADASTRO DE PERFIL", self.LARANJA, self.AMBAR))
        print(gradiente_texto("=" * 60, self.AMBAR, self.ACO_ESCURO))

        try:
            nome = validar_nome_perfil(
                input(gradiente_texto("Nome (coordenador/gestor/professor/aluno/representante): ", self.ACO_ESCURO, self.LARANJA))
            )
            descricao = input(gradiente_texto("Descrição: ", self.LARANJA, self.AMBAR))

        except ValueError as erro:
            print()
            print(gradiente_texto(f"Erro: {erro}", self.AMBAR, self.ACO_ESCURO))
            input("\nPressione ENTER para continuar...")
            return

        perfil = Perfil(
            nome=nome,
            descricao=descricao
        )
        self.repository.salvar(perfil)
        print()
        input("Pressione ENTER para continuar...")

    def buscar_perfil(self):
        print()
        print(gradiente_texto("=" * 60, self.ACO_ESCURO, self.AMBAR))
        print(gradiente_texto("BUSCAR PERFIL", self.LARANJA, self.AMBAR))
        print(gradiente_texto("=" * 60, self.AMBAR, self.ACO_ESCURO))

        try:
            id_perfil = int(
                input(gradiente_texto("Código do perfil: ", self.ACO_ESCURO, self.LARANJA))
            )

        except ValueError:
            print()
            print("Código inválido.")
            input("\nPressione ENTER para continuar...")
            return

        perfil = self.repository.buscar_por_id(id_perfil)
        print()

        if perfil is None:
            print("Perfil não encontrado.")

        else:
            print(gradiente_texto(f"Código......: {perfil.id_perfil}", self.ACO_ESCURO, self.LARANJA))
            print(gradiente_texto(f"Nome........: {perfil.nome}", self.LARANJA, self.AMBAR))
            print(gradiente_texto(f"Descrição...: {perfil.descricao}", self.AMBAR, self.ACO_ESCURO))

        print()
        input("Pressione ENTER para continuar...")

    def listar_perfil(self):
        print()
        print(gradiente_texto("=" * 60, self.ACO_ESCURO, self.AMBAR))
        print(gradiente_texto("LISTA DE PERFIS", self.LARANJA, self.AMBAR))
        print(gradiente_texto("=" * 60, self.AMBAR, self.ACO_ESCURO))
        perfis = self.repository.listar()

        if not perfis:
            print()
            print("Nenhum perfil cadastrado.")
            print()
            input("Pressione ENTER para continuar...")
            return

        print(
            gradiente_texto(
                f"{'ID':<5}{'Nome':<20}{'Descrição':<35}",
                self.ACO_ESCURO, self.AMBAR
            )
        )
        print(gradiente_texto("-" * 60, self.AMBAR, self.ACO_ESCURO))

        for perfil in perfis:
            print(
                gradiente_texto(
                    f"{perfil.id_perfil:<5}{perfil.nome:<20}{(perfil.descricao or ''):<35}",
                    self.LARANJA, self.AMBAR
                )
            )

        print()
        print(gradiente_texto(f"Total de perfis: {len(perfis)}", self.LARANJA, self.AMBAR))
        print()
        input("Pressione ENTER para continuar...")

    def atualizar_perfil(self):
        print()
        print(gradiente_texto("=" * 60, self.ACO_ESCURO, self.AMBAR))
        print(gradiente_texto("ATUALIZAÇÃO DE PERFIL", self.LARANJA, self.AMBAR))
        print(gradiente_texto("=" * 60, self.AMBAR, self.ACO_ESCURO))

        try:
            id_perfil = int(
                input(gradiente_texto("Código do perfil: ", self.ACO_ESCURO, self.LARANJA))
            )

        except ValueError:
            print()
            print("Código inválido.")
            input("\nPressione ENTER para continuar...")
            return

        perfil = self.repository.buscar_por_id(id_perfil)

        if perfil is None:
            print()
            print("Perfil não encontrado.")
            input("\nPressione ENTER para continuar...")
            return

        print()
        print(gradiente_texto("Pressione ENTER para manter o valor atual.", self.LARANJA, self.AMBAR))
        print()

        nome = input(
            gradiente_texto(f"Nome [{perfil.nome}]: ", self.ACO_ESCURO, self.LARANJA)
        )
        if nome:
            try:
                perfil.nome = validar_nome_perfil(nome)
            except ValueError as erro:
                print(gradiente_texto(f"Erro: {erro}", self.AMBAR, self.ACO_ESCURO))
                input("\nPressione ENTER para continuar...")
                return

        descricao = input(
            gradiente_texto(f"Descrição [{perfil.descricao}]: ", self.LARANJA, self.AMBAR)
        )
        if descricao:
            perfil.descricao = descricao

        self.repository.atualizar(perfil)
        print()
        input("Pressione ENTER para continuar...")

    def excluir_perfil(self):
        print()
        print(gradiente_texto("=" * 60, self.ACO_ESCURO, self.AMBAR))
        print(gradiente_texto("EXCLUSÃO DE PERFIL", self.LARANJA, self.AMBAR))
        print(gradiente_texto("=" * 60, self.AMBAR, self.ACO_ESCURO))

        try:
            id_perfil = int(
                input(gradiente_texto("Código do perfil: ", self.ACO_ESCURO, self.LARANJA))
            )

        except ValueError:
            print()
            print("Código inválido.")
            input("\nPressione ENTER para continuar...")
            return

        perfil = self.repository.buscar_por_id(id_perfil)

        if perfil is None:
            print()
            print("Perfil não encontrado.")
            input("\nPressione ENTER para continuar...")
            return

        print()
        print(gradiente_texto("Perfil localizado", self.LARANJA, self.AMBAR))
        print(gradiente_texto("-" * 60, self.AMBAR, self.ACO_ESCURO))
        print(gradiente_texto(f"Código.....: {perfil.id_perfil}", self.ACO_ESCURO, self.LARANJA))
        print(gradiente_texto(f"Nome.......: {perfil.nome}", self.LARANJA, self.AMBAR))
        print()

        resposta = input(
            gradiente_texto("Deseja realmente excluir este perfil? (S/N): ", self.AMBAR, self.ACO_ESCURO)
        ).strip().upper()

        if resposta != "S":
            print()
            print("Operação cancelada.")
            input("\nPressione ENTER para continuar...")
            return

        self.repository.excluir(id_perfil)
        print()
        input("Pressione ENTER para continuar...")
```

## 6. `main.py`

```python
from menus.menu_principal import MenuPrincipal

def main():
    menu = MenuPrincipal()
    menu.exibir()

if __name__ == "__main__":
    main()
```

## 7. `database/conexao.py` e `database/criar_tabelas.py`

Esses dois já são genéricos (servem para todas as classes, não precisam ser
recriados por classe) — só copie do repositório uma vez:

```python
# database/conexao.py
import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv() #carrega automaticamente as variaveis existentes no .env

class Conexao:
    def __init__(self):
        self.host = os.getenv("DB_HOST")
        self.port = os.getenv("DB_PORT", "3306")
        self.database = os.getenv("DB_NAME")
        self.user = os.getenv("DB_USER")
        self.password = os.getenv("DB_PASSWORD")
        self.ssl_ca = os.getenv("DB_SSL_CA")  # caminho do certificado da Aiven (ca.pem)

        argumentos_conexao = {
            "host": self.host,
            "port": int(self.port),
            "database": self.database,
            "user": self.user,
            "password": self.password,
        }

        # Aiven exige conexão criptografada. Se o caminho do certificado
        # estiver configurado no .env, a conexão usa SSL.
        if self.ssl_ca:
            argumentos_conexao["ssl_ca"] = self.ssl_ca
            argumentos_conexao["ssl_verify_cert"] = True

        self.conexao = mysql.connector.connect(**argumentos_conexao)
        self.cursor = self.conexao.cursor()

    def commit(self):
        self.conexao.commit()
    def rollback(self):
        self.conexao.rollback()
    def fechar(self):
        self.cursor.close()
        self.conexao.close()
```

```python
# database/criar_tabelas.py
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
```

## 8. `requirements.txt`

```
mysql-connector-python==9.1.0
python-dotenv==1.0.1
```

---

## Como adaptar para a próxima classe

Troque, em todos os blocos acima:
- `perfis` → nome da nova tabela (ex: `usuarios`)
- `Perfil` / `perfil` → nome da nova classe (ex: `Usuario` / `usuario`)
- `id_perfil` → `id_<nova_classe>`
- Os campos do `__init__`, do `INSERT`/`UPDATE` e das colunas do `SELECT *` conforme as colunas da nova tabela

**Tabela:** crie `database/tabelas/<N>_<sua_tabela>.sql` — **nunca edite o
`.sql` de outra classe.** Pegue o próximo número livre (ex: se o maior já
existente é `13_calendario_preventivo.sql`, o seu é `14_...`); se sua tabela
tem FK pra uma tabela que ainda não existe, escolha um número maior que o
dela. `criar_tabelas.py` executa os arquivos nessa ordem automaticamente —
não precisa editá-lo.

`database/conexao.py` e `main.py` não mudam.

Na pasta `menus/`:
- **Crie `menus/<sua_classe>_menu.py`** copiando a estrutura de
  `menus/perfil_menu.py` — **nunca edite o arquivo de outra classe.**
- **Só toque em `menus/menu_principal.py` pra adicionar 2 linhas**: o
  `import` da sua classe no topo e a opção nova (`elif opcao == "2":
  MenuNovaClasse().exibir()`) — sem mexer nas linhas de quem já está lá.
  `MenuPrincipal` é único e fica sempre azul, não crie um segundo.
- Dê ao seu submenu **uma paleta de cores diferente das já usadas** (defina
  3 tons próprios, tipo: `AZUL_MARINHO/AZUL_ACO/AZUL_CLARO` do principal,
  `ACO_ESCURO/LARANJA/AMBAR` do Perfil — escolha outra combinação, ex: verde,
  roxo, vermelho...). Isso ajuda a distinguir visualmente em qual módulo do
  sistema a pessoa está.
- `menus/gradiente.py` também não muda — só importe `gradiente_texto` dele.

Tabela de cores já usadas (para não repetir):

| Classe | Menu | Cores |
|---|---|---|
| — | `MenuPrincipal` | Azul (marinho → aço → claro) |
| Perfil | `MenuPerfil` | Laranja (aço escuro → laranja → âmbar) |
| Turma | `MenuTurma` | Verde (escuro → verde → claro) |
| Usuario | `MenuUsuario` | Roxo (escuro → roxo → lilás claro) |
| LogAuditoria | `MenuLogAuditoria` | Vermelho (escuro → vermelho → rosa claro) |
| Setor | `MenuSetor` | Amarelo (âmbar escuro → amarelo → amarelo claro) |
| Maquina | `MenuMaquina` | Ciano (teal escuro → teal → teal claro) |

No `utils/`: crie `utils/<sua_classe>_validacoes.py` (nunca edite o arquivo
de outra classe) e importe `validar_campo_obrigatorio` de
`utils/validacoes_gerais.py` quando precisar de uma validação genérica.
