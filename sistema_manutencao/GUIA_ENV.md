# Guia — Configurar o `.env`

O projeto não roda com credenciais reais dentro do código (isso seria
um risco de segurança e vazaria a senha do banco pro GitHub). Em vez
disso, cada pessoa tem seu próprio arquivo `.env` **local**, que nunca é
commitado (já está no `.gitignore`).

## Passo 1 — Copiar o modelo

Dentro da pasta `sistema_manutencao/`, rode:

```bash
cp .env.example .env
```

Isso cria o arquivo `.env` com a mesma estrutura do `.env.example`, mas
esse novo arquivo é só seu — pode editar à vontade, ele não vai pro Git.

## Passo 2 — Pegar as credenciais reais na Aiven

1. Entre no [console da Aiven](https://console.aiven.io/) e abra o serviço do banco (PostgreSQL).
2. Na aba **Overview** do serviço, vai ter um bloco "Connection Information" com:
   - **Host**
   - **Port**
   - **Database name**
   - **User**
   - **Password**
3. Copie cada um desses valores.

## Passo 3 — Preencher o `.env`

Abra o `.env` que você criou no Passo 1 e troque os valores de exemplo pelos reais:

```env
DB_HOST=pg-xxxxxxx-projeto.aivencloud.com
DB_PORT=5432
DB_NAME=defaultdb
DB_USER=avnadmin
DB_PASSWORD=
DB_SSLMODE=require
```

| Variável | O que é | Onde pegar |
|---|---|---|
| `DB_HOST` | Endereço do servidor Postgres | Campo **Host** na Aiven |
| `DB_PORT` | Porta de conexão (normalmente `5432` na Aiven, mas confira — às vezes vem uma porta diferente) | Campo **Port** na Aiven |
| `DB_NAME` | Nome do banco | Campo **Database name** na Aiven — no plano gratuito costuma vir `defaultdb` |
| `DB_USER` | Usuário do banco | Campo **User** na Aiven — geralmente `avnadmin` |
| `DB_PASSWORD` | Senha do banco | Campo **Password** na Aiven |
| `DB_SSLMODE` | Exige conexão criptografada | Deixe `require` — a Aiven não aceita conexão sem SSL |

**Não deixe espaços** em volta do `=` (`DB_HOST=valor`, não `DB_HOST = valor`) e **não use aspas** em volta do valor.

## Passo 4 — Testar a conexão

Com o `.env` preenchido, rode dentro de `sistema_manutencao/`:

```bash
pip install -r requirements.txt
python -c "from database.conexao import Conexao; Conexao(); print('Conectou com sucesso!')"
```

Se aparecer `Conectou com sucesso!`, está tudo certo. Se der erro:
- `password authentication failed` → confira `DB_USER`/`DB_PASSWORD`.
- `could not translate host name` → confira `DB_HOST` (copiou errado ou tem espaço sobrando).
- erro de SSL → confira se `DB_SSLMODE=require` está lá.

## Se ainda não existirem as tabelas no banco

Depois que a conexão funcionar, crie o schema (só precisa rodar uma vez por banco):

```bash
python -c "from database.criar_tabelas import criar_tabelas; criar_tabelas()"
```

## Lembrete de segurança

- **Nunca** apague a linha `.env` do `.gitignore`.
- **Nunca** cole sua senha do `.env` no chat do grupo, no Trello ou em qualquer commit — se isso acontecer, troque a senha na Aiven imediatamente.
- Cada pessoa do time usa o **mesmo banco** (a mesma Aiven), então o `.env` de todo mundo tem os mesmos valores — só não compartilhem o arquivo em texto aberto em lugar público.
