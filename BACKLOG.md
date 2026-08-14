# Backlog — Sistema de Gerenciamento de Manutenção (CTW)

Baseado no schema `ctw_manutencao` (13 tabelas) e na estrutura de pastas `sistema_manutencao/` (database / models / repositories / utils / menu.py / main.py). Organizado em 6 épicos = 6 bancadas (3 código + 3 documentação, 22 pessoas).

Convenção de cartão Trello: `[MÓDULO] Ação — entidade` · Labels: `backend`, `frontend`, `doc`, `banco`, `bug`. Cada história tem tarefas técnicas mapeadas em arquivo/pasta e critérios de aceite.

---

## Divisão das 6 bancadas

| Bancada | Tipo | Módulos (tabelas) |
|---|---|---|
| **Bancada 1 — Código** | Backend | Auth/RBAC + Mapa da Oficina: `perfis`, `turmas`, `usuarios`, `logs_auditoria`, `setores`, `maquinas` |
| **Bancada 2 — Código** | Backend | Almoxarifado/Ferramentaria + Preventivo: `itens_almoxarifado`, `alertas_estoque`, `registros_quebra`, `calendario_preventivo` |
| **Bancada 3 — Código** | Backend | SS/OS + Compras: `solicitacoes_servico`, `ordens_servico`, `solicitacoes_compras` |
| **Bancada 4 — Documentação** | Doc | Espelha Bancada 1: dicionário de dados, DER, manual do usuário (login/perfis), regras de RBAC |
| **Bancada 5 — Documentação** | Doc | Espelha Bancada 2: dicionário de dados, manual do almoxarifado, fluxo de alertas/quebra, Portal Notion (formulários) |
| **Bancada 6 — Documentação** | Doc | Espelha Bancada 3: dicionário de dados, fluxo SS→OS, manual de compras, POP (procedimento operacional padrão) |

Cada bancada de documentação trabalha em paralelo com a bancada de código correspondente e valida as telas/menus que ela produz.

---

## Épico 0 — Fundação do Projeto (transversal, feito uma vez)

- [ ] **[SETUP] Criar repositório Git de código** — `sistema_manutencao/`, `.gitignore`, `requirements.txt`, README com instruções de setup
- [ ] **[SETUP] Criar repositório Git de documentação** — separado, com pastas `der/`, `dicionario-dados/`, `manuais/`, `pop/`
- [ ] **[SETUP] Configurar `database/conexao.py`** — conexão MySQL parametrizada via `.env` (host, user, senha, db)
- [ ] **[SETUP] Rodar `database/schema.sql`** — criar banco `ctw_manutencao` e as 13 tabelas
- [ ] **[SETUP] Popular dados de seed** — `perfis` (Coordenador, Gestor, Professor, Aluno, Representante), `turmas`, `setores` iniciais
- [ ] **[SETUP] Criar quadro Trello** — 1 lista por módulo (Backlog / A Fazer / Em Andamento / Revisão / Concluído), cartões deste backlog
- [ ] **[SETUP] Definir template de card e checklist de Definition of Done** (código: testado + revisado; doc: revisado por 2 pessoas)

---

## Épico 1 — Autenticação e RBAC (Bancada 1 / Bancada 4)

Tabelas: `perfis`, `usuarios`, `turmas`, `logs_auditoria`

### Backend
- [ ] **[AUTH] Model `Perfil`** — `models/perfil.py` (id, nome, descricao)
- [ ] **[AUTH] Model `Turma`** — `models/turma.py` (id, codigo, periodo)
- [ ] **[AUTH] Model `Usuario`** — `models/usuario.py` (id, perfil_id, turma_id, nome, email, senha_hash, criado_em)
- [ ] **[AUTH] Model `LogAuditoria`** — `models/log_auditoria.py`
- [ ] **[AUTH] Repository CRUD `PerfilRepository`** — `repositories/perfil_repository.py`
- [ ] **[AUTH] Repository CRUD `TurmaRepository`** — `repositories/turma_repository.py`
- [ ] **[AUTH] Repository CRUD `UsuarioRepository`** — `repositories/usuario_repository.py` (inclui busca por email, listar por turma/perfil)
- [ ] **[AUTH] Repository `LogAuditoriaRepository`** — apenas `criar` e `listar` (somente leitura/inserção, sem update/delete)
- [ ] **[AUTH] Hash de senha** — `utils/validacoes.py` usando `bcrypt`/`hashlib` (nunca salvar senha em texto puro)
- [ ] **[AUTH] Validação de email e perfil** — `utils/validacoes.py`
- [ ] **[AUTH] Função `login(email, senha)`** — valida credenciais, retorna usuário + perfil, grava log de acesso
- [ ] **[AUTH] Middleware/checagem de permissão por perfil** — decorator ou função `exige_perfil(usuario, perfis_permitidos)`
- [ ] **[AUTH] Menu CRUD de usuários/turmas/perfis** — `menu.py` (submenu "Administração")
- [ ] **[AUTH] Relatório: usuários por turma/perfil** — opção de relatório no menu

### Documentação (Bancada 4)
- [ ] **[DOC-AUTH] Dicionário de dados** — `perfis`, `usuarios`, `turmas`, `logs_auditoria`
- [ ] **[DOC-AUTH] DER do módulo de autenticação**
- [ ] **[DOC-AUTH] Matriz de permissões por perfil** (o que cada perfil pode ver/criar/editar/excluir em cada módulo)
- [ ] **[DOC-AUTH] Manual do usuário — login e cadastro**
- [ ] **[DOC-AUTH] POP — cadastro de turma/aluno no início do semestre**

---

## Épico 2 — Mapa da Oficina e Maquinário (Bancada 1 / Bancada 4)

Tabelas: `setores`, `maquinas`

### Backend
- [ ] **[MAQ] Model `Setor`** — `models/setor.py`
- [ ] **[MAQ] Model `Maquina`** — `models/maquina.py` (tag, nome, status_vivo, ultima_manutencao)
- [ ] **[MAQ] Repository CRUD `SetorRepository`**
- [ ] **[MAQ] Repository CRUD `MaquinaRepository`** — incluir `atualizar_status`, `listar_por_setor`, `listar_por_status`
- [ ] **[MAQ] Validação de tag única (ex: TOR-01)** — `utils/validacoes.py`
- [ ] **[MAQ] Importar/cadastrar máquinas a partir do PDF do Centroweg** — script `database/importar_maquinas.py` (entrada manual ou CSV extraído do PDF)
- [ ] **[MAQ] Menu CRUD de setores e máquinas**
- [ ] **[MAQ] Relatório: máquinas por status (Operando/Manutenção/Parado/Crítico)**
- [ ] **[MAQ] Relatório: máquinas sem manutenção há mais de X dias**

### Documentação (Bancada 4)
- [ ] **[DOC-MAQ] Dicionário de dados** — `setores`, `maquinas`
- [ ] **[DOC-MAQ] Planilha/lista consolidada de máquinas** (a partir do PDF do Centroweg) com tag padronizada
- [ ] **[DOC-MAQ] Manual — cadastro e mapa de máquinas por setor**

---

## Épico 3 — Almoxarifado, Ferramentaria e Registro de Quebra (Bancada 2 / Bancada 5)

Tabelas: `itens_almoxarifado`, `alertas_estoque`, `registros_quebra`

### Backend
- [ ] **[ALM] Model `ItemAlmoxarifado`** — `models/item_almoxarifado.py`
- [ ] **[ALM] Model `AlertaEstoque`** — `models/alerta_estoque.py`
- [ ] **[ALM] Model `RegistroQuebra`** — `models/registro_quebra.py`
- [ ] **[ALM] Repository CRUD `ItemAlmoxarifadoRepository`** — incluir `dar_baixa`/`dar_entrada` (movimentação de estoque)
- [ ] **[ALM] Repository `AlertaEstoqueRepository`** — criar/resolver alerta
- [ ] **[ALM] Repository CRUD `RegistroQuebraRepository`** — incluir upload/armazenamento de `foto_url`
- [ ] **[ALM] Trigger/regra de negócio: gerar alerta automático quando `quantidade_atual < estoque_minimo`** — no repository, após cada baixa de estoque
- [ ] **[ALM] Menu CRUD de itens do almoxarifado**
- [ ] **[ALM] Menu: registrar quebra de ferramenta/item** (formulário simples: item, usuário, descrição, foto)
- [ ] **[ALM] Menu: painel de alertas pendentes**
- [ ] **[ALM] Relatório: itens abaixo do estoque mínimo**
- [ ] **[ALM] Relatório: histórico de quebras por item/usuário/período**

### Documentação (Bancada 5)
- [ ] **[DOC-ALM] Dicionário de dados** — `itens_almoxarifado`, `alertas_estoque`, `registros_quebra`
- [ ] **[DOC-ALM] Manual — controle de estoque da ferramentaria**
- [ ] **[DOC-ALM] POP — registro de quebra de ferramenta/item**
- [ ] **[DOC-ALM] Formulário Notion (Portal da Manutenção) — Registro de Quebra**

---

## Épico 4 — Calendário Preventivo (Bancada 2 / Bancada 5)

Tabela: `calendario_preventivo`

### Backend
- [ ] **[CAL] Model `CalendarioPreventivo`** — `models/calendario_preventivo.py`
- [ ] **[CAL] Repository CRUD `CalendarioPreventivoRepository`** — incluir `listar_por_periodo`, `marcar_concluida`, `recalcular_proxima_data` (baseado na `frequencia`)
- [ ] **[CAL] Regra: ao concluir uma manutenção preventiva, gerar próxima ocorrência automaticamente** (soma a frequência à data)
- [ ] **[CAL] Job/rotina para marcar como "Atrasada"** quando `data_proxima_execucao < hoje` e status ainda "Agendada"
- [ ] **[CAL] Menu CRUD do calendário preventivo por máquina/turma**
- [ ] **[CAL] Relatório: agenda da semana/mês**
- [ ] **[CAL] Relatório: preventivas atrasadas**

### Documentação (Bancada 5)
- [ ] **[DOC-CAL] Dicionário de dados** — `calendario_preventivo`
- [ ] **[DOC-CAL] Manual — planejamento de manutenção preventiva**
- [ ] **[DOC-CAL] Modelo de calendário preventivo (Notion/planilha) por setor**

---

## Épico 5 — Solicitação de Serviço (S.S.) e Ordem de Serviço (O.S.) (Bancada 3 / Bancada 6)

Tabelas: `solicitacoes_servico`, `ordens_servico`

### Backend
- [ ] **[SSOS] Model `SolicitacaoServico`** — `models/solicitacao_servico.py`
- [ ] **[SSOS] Model `OrdemServico`** — `models/ordem_servico.py`
- [ ] **[SSOS] Repository CRUD `SolicitacaoServicoRepository`** — incluir `atualizar_status`, `listar_por_status/maquina/solicitante`
- [ ] **[SSOS] Repository CRUD `OrdemServicoRepository`** — incluir `abrir_a_partir_de_ss(solicitacao_id)`
- [ ] **[SSOS] Máquina de estados da S.S.** — Aberta → Em Análise → Aguardando Peças → Execução → Validação → Concluída (validar transições permitidas em `utils/validacoes.py`)
- [ ] **[SSOS] Regra: ao concluir a O.S., atualizar `maquinas.status_vivo` e `ultima_manutencao`**
- [ ] **[SSOS] Menu: abrir Solicitação de Serviço** (aluno/professor)
- [ ] **[SSOS] Menu: triagem de S.S.** (mudar status, atribuir responsável/professor validador)
- [ ] **[SSOS] Menu: registrar execução (O.S.)** — descrição, peças usadas, datas/horas, quantidade de pessoas
- [ ] **[SSOS] Relatório: SS abertas por prioridade/máquina**
- [ ] **[SSOS] Relatório: tempo médio entre abertura da SS e conclusão da OS**
- [ ] **[SSOS] Relatório: OS por tipo de manutenção (Corretiva/Preventiva/Preditiva/Melhoria)**

### Documentação (Bancada 6)
- [ ] **[DOC-SSOS] Dicionário de dados** — `solicitacoes_servico`, `ordens_servico`
- [ ] **[DOC-SSOS] Fluxograma do ciclo SS → OS**
- [ ] **[DOC-SSOS] Manual do usuário — abrir e acompanhar uma SS**
- [ ] **[DOC-SSOS] Formulário Notion (Portal da Manutenção) — Solicitação de Manutenção / Livro Máquina** (ajustar formulário existente ao novo fluxo SS/OS)

---

## Épico 6 — Solicitação de Compras (Bancada 3 / Bancada 6)

Tabela: `solicitacoes_compras`

### Backend
- [ ] **[COMP] Model `SolicitacaoCompra`** — `models/solicitacao_compra.py`
- [ ] **[COMP] Repository CRUD `SolicitacaoCompraRepository`** — incluir `atualizar_status`, `listar_por_status/turma/maquina`
- [ ] **[COMP] Validação de campos obrigatórios** (especificação técnica, justificativa, professor responsável)
- [ ] **[COMP] Upload/anexo de arquivos** (`arquivos` — orçamento, foto da peça)
- [ ] **[COMP] Menu: abrir solicitação de compra**
- [ ] **[COMP] Menu: acompanhar status** (Não Visualizado → Em Análise → Pedido em Andamento → Entregue)
- [ ] **[COMP] Relatório: solicitações por status/turma**
- [ ] **[COMP] Relatório: tempo médio de atendimento de compras**

### Documentação (Bancada 6)
- [ ] **[DOC-COMP] Dicionário de dados** — `solicitacoes_compras`
- [ ] **[DOC-COMP] Manual — como abrir uma solicitação de compra**
- [ ] **[DOC-COMP] Formulário Notion (Portal da Manutenção) — Solicitação de Compras** (revisar campos existentes contra a tabela nova)

---

## Épico 7 — Interface e Integração (transversal — depois que os módulos acima estiverem estáveis)

- [ ] **[UI] Menu principal `menu.py`** — login, roteamento por perfil, submenus por módulo
- [ ] **[UI] Padronizar telas de CRUD genérico** — listar / criar / editar / excluir / buscar, reaproveitável entre módulos
- [ ] **[UI] Tela/opção "Relatórios"** — escolher relatório e exportar (texto, CSV ou PDF simples)
- [ ] **[UI] (opcional) Interface web simples** — se houver tempo, Flask/FastAPI + templates básicos reaproveitando os repositories já prontos
- [ ] **[INT] Alinhar Portal da Manutenção (Notion) com o banco** — mapear cada formulário Notion existente para a tabela correspondente, decidir se o Notion alimenta o banco (importação) ou é substituído pelo sistema
- [ ] **[INT] Teste integrado ponta a ponta** — abrir SS → gerar OS → atualizar máquina → abrir compra vinculada → concluir
- [ ] **[INT] Testes automatizados dos repositories** (`pytest`, ao menos casos de CRUD básico por módulo)

---

## Backlog de Documentação Geral (transversal)

- [ ] **[DOC] Documento consolidado do banco de dados** — schema completo + dicionário de dados + DER geral (junta os 6 DERs parciais das bancadas)
- [ ] **[DOC] Manual do usuário completo** (compilando os manuais de cada módulo)
- [ ] **[DOC] Guia de instalação/setup do sistema**
- [ ] **[DOC] Relatório final de testes**

---

### Como usar no Trello
Crie uma lista por Épico (0 a 7) e um cartão por item acima, com o prefixo `[MÓDULO]` já no título. Marque a bancada responsável como membro do cartão e use os labels `backend`/`doc`/`banco`/`frontend` para filtrar. As bancadas de documentação devem linkar seus cartões aos cartões de backend equivalentes (mesma tabela/módulo) para manter o paralelismo.
