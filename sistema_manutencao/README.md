# Sistema de Gerenciamento de Manutenção (THAF)

Backend em Python (arquitetura em camadas: `models` / `repositories` / `database` / `utils`) para o setor de manutenção, rodando sobre **PostgreSQL** hospedado na Aiven, com **soft delete** em todas as tabelas.

Ver `../BACKLOG.md` na raiz do repositório para o backlog completo por módulo/bancada e `../NOTION_TEMPLATE_CLASSE.md` para o passo a passo de como criar uma nova classe.

## Estrutura

```
sistema_manutencao/
├── database/
│   ├── conexao.py         # classe Conexao (psycopg, lê .env, sslmode p/ Aiven)
│   ├── criar_tabelas.py   # roda todos os .sql de tabelas/ na ordem certa
│   └── tabelas/
│       ├── 00_tipos.sql     # ENUMs compartilhados
│       ├── 00_funcoes.sql   # funções de trigger compartilhadas (soft delete)
│       └── <numero>_<tabela>.sql  # uma tabela por arquivo (numerado p/ respeitar as FKs)
├── models/                 # uma classe simples por entidade (__init__ + __str__)
├── repositories/           # uma classe por entidade: salvar/buscar_por_id/listar/atualizar/excluir
├── utils/
│   ├── validacoes_gerais.py   # validações genéricas compartilhadas
│   └── <classe>_validacoes.py # validações específicas de cada classe
├── menus/
│   ├── gradiente.py         # gradiente_texto() compartilhado
│   ├── menu_principal.py    # MenuPrincipal (azul, único) — lista os módulos
│   └── <classe>_menu.py     # submenu completo de cada classe, cor própria
├── main.py                 # ponto de entrada
└── requirements.txt
```

**Por que um arquivo por tabela/classe/validação/menu?** Com várias pessoas
trabalhando ao mesmo tempo, cada uma mexe só nos arquivos da sua própria
classe — evita conflito de merge. Os únicos pontos compartilhados são
`menus/menu_principal.py` (2 linhas por classe: import + opção) e,
ocasionalmente, `utils/validacoes_gerais.py`, `database/tabelas/00_tipos.sql`
e `database/tabelas/00_funcoes.sql`. Detalhes em `../NOTION_TEMPLATE_CLASSE.md`.

## Soft delete — dois padrões, dependendo da tabela

- **In-place** (`perfis`, `turmas`, `setores`): a tabela tem uma coluna
  `deleted_at`. Um `DELETE` é interceptado por trigger e vira
  `UPDATE deleted_at = now()` — a linha nunca some fisicamente. Por isso
  **toda query de leitura precisa filtrar `WHERE deleted_at IS NULL`**, e o
  `cursor.rowcount` do `DELETE` não é confiável (o trigger cancela o delete
  físico) — `excluir()` sempre confere com `buscar_por_id()` antes.
- **Herança** (as demais tabelas: `usuarios`, `logs_auditoria`, `maquinas`...):
  um `DELETE` move a linha inteira para `<tabela>_deletados` via trigger. O
  Postgres, por padrão, inclui as linhas da tabela filha quando você faz
  `SELECT * FROM tabela` — por isso **toda query de leitura usa
  `FROM ONLY <tabela>`** para trazer só os registros ativos.

Ao criar uma classe nova, confira em `database/tabelas/<numero>_<tabela>.sql`
qual dos dois padrões a tabela usa e siga o repository de `Perfil` (in-place)
ou de `Usuario`/`Maquina` (herança) como referência.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # preencher credenciais da Aiven (Postgres)
python -c "from database.criar_tabelas import criar_tabelas; criar_tabelas()"
python main.py
```

## Convenções

- Toda query usa parâmetros (`%s`) — nunca concatenar strings SQL.
- Repositories seguem sempre o mesmo padrão: `criar_<entidade>` (monta o objeto a partir da tupla do banco), `salvar`, `buscar_por_id`, `listar`, `atualizar`, `excluir`, `fechar`, com `try/except` fazendo `rollback` e print do erro.
- Cada classe nova cria seu próprio arquivo em `models/`, `repositories/`, `utils/`, `menus/` e um novo `.sql` numerado em `database/tabelas/` — nunca edite o arquivo de outra classe.
- Cada classe ganha um submenu próprio (`menus/<classe>_menu.py`) com uma paleta de cores (`gradiente_texto`) diferente das já usadas. O `MenuPrincipal` (azul) é único; só recebe 2 linhas novas por classe (import + opção).
