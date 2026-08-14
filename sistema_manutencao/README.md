# Sistema de Gerenciamento de Manutenção (THAF)

Backend em Python (arquitetura em camadas: `models` / `repositories` / `database` / `utils`) para o setor de manutenção, rodando sobre MySQL hospedado na Aiven.

Ver `../BACKLOG.md` na raiz do repositório para o backlog completo por módulo/bancada e `../NOTION_TEMPLATE_CLASSE.md` para o passo a passo de como criar uma nova classe.

## Estrutura

```
sistema_manutencao/
├── database/
│   ├── conexao.py         # classe Conexao (mysql-connector, lê .env, suporta SSL da Aiven)
│   ├── criar_tabelas.py   # roda todos os .sql de tabelas/ na ordem certa
│   └── tabelas/            # um arquivo .sql por tabela (numerado p/ respeitar as FKs)
├── models/                 # uma classe simples por entidade (__init__ + __str__)
├── repositories/           # uma classe por entidade: salvar/buscar_por_id/listar/atualizar/excluir
├── utils/
│   ├── validacoes_gerais.py   # validações genéricas compartilhadas
│   └── <classe>_validacoes.py # validações específicas de cada classe
├── menu.py                 # MenuPrincipal (azul) + um submenu colorido por classe
├── main.py                 # ponto de entrada
└── requirements.txt
```

**Por que um arquivo por tabela/classe/validação?** Com várias pessoas
trabalhando ao mesmo tempo, cada uma mexe só nos arquivos da sua própria
classe — evita conflito de merge. Os únicos pontos compartilhados são
`menu.py` (adicionar uma opção no `MenuPrincipal`) e, ocasionalmente,
`utils/validacoes_gerais.py`. Detalhes em `../NOTION_TEMPLATE_CLASSE.md`.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # preencher credenciais da Aiven (inclui DB_SSL_CA)
python database/criar_tabelas.py   # cria as tabelas em database/tabelas/
python main.py
```

## Convenções

- Toda query usa parâmetros (`%s`) — nunca concatenar strings SQL.
- Repositories seguem sempre o mesmo padrão: `criar_<entidade>` (monta o objeto a partir da tupla do banco), `salvar`, `buscar_por_id`, `listar`, `atualizar`, `excluir`, `fechar`, com `try/except` fazendo `rollback` e print do erro.
- Cada classe nova cria seu próprio arquivo em `models/`, `repositories/`, `utils/` e um novo `.sql` numerado em `database/tabelas/` — nunca edite o arquivo de outra classe.
- Cada classe ganha um submenu próprio em `menu.py`, com uma paleta de cores (`gradiente_texto`) diferente das já usadas. O `MenuPrincipal` (azul) é único.
