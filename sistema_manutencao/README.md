# Sistema de Gerenciamento de Manutenção (CTW)

Backend em Python (arquitetura em camadas: `models` / `repositories` / `database` / `utils`) para o setor de manutenção, cobrindo: autenticação/RBAC, mapa da oficina e máquinas, almoxarifado/ferramentaria, registro de quebra, Solicitação de Serviço (SS) e Ordem de Serviço (OS), solicitação de compras e calendário preventivo.

Ver `../BACKLOG.md` na raiz do repositório para o backlog completo por módulo/bancada.

## Estrutura

```
sistema_manutencao/
├── database/
│   ├── conexao.py       # pool de conexão MySQL (lê .env)
│   ├── criar_tabelas.py # cria o banco e as tabelas a partir do schema.sql
│   └── schema.sql       # DDL completo (13 tabelas)
├── models/               # dataclasses das entidades
├── repositories/         # CRUD + regras de acesso a dados por entidade
├── utils/
│   └── validacoes.py     # validações, hash de senha, checagem de perfil
├── menu.py                # menu CLI com login + CRUD por módulo
├── main.py                # ponto de entrada
└── requirements.txt
```

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # preencher credenciais do MySQL
python database/criar_tabelas.py   # cria o banco ctw_manutencao
python main.py
```

## Primeiro acesso

O banco não vem com usuário padrão. Cadastre manualmente o primeiro registro em `perfis` (ex: `coordenador`) e o primeiro `usuario` direto no banco (com senha já hasheada via `utils.validacoes.gerar_hash_senha`), ou crie um script `seed.py` conforme o item `[SETUP] Popular dados de seed` do backlog.

## Convenções

- Toda query usa parâmetros (`%s`) — nunca concatenar strings SQL.
- Senhas são armazenadas apenas com hash (`bcrypt`), nunca em texto puro.
- Regras de negócio (ex.: transições de status da SS, geração de alerta de estoque, próxima ocorrência do calendário preventivo) ficam nos `repositories`, não no `menu.py`.
