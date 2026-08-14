# Template Notion — Passo a passo de uma Classe

Modelo para criar, no Notion, um card por classe/tabela do sistema — no mesmo
formato usado no card "Perfis" (Tabela SQL / Classe / Comando do Git / Código
da Tabela). Duplique esta página para cada classe do backlog e preencha os
campos entre `< >`.

---

## 🔧 Template em branco

**Tabela SQL:** `<nome_da_tabela>`
**Classe:** `<NomeDaClasse>`
**Comando do Git:**
```
git checkout -b "Feature/Issue-#<N>/<NomeDaClasse>"
```

**Código da Tabela do Banco de Dados:**
```sql
CREATE TABLE <nome_da_tabela> (
    ...
);
```

**Passo a passo de implementação:**
1. `git checkout -b "Feature/Issue-#<N>/<NomeDaClasse>"`
2. Adicionar o `CREATE TABLE` em `database/schema.sql`
3. Criar `models/<nome_da_classe>.py` — classe simples com `__init__` e `__str__`
4. Criar `repositories/<nome_da_classe>_repository.py` — `criar_<entidade>`, `salvar`, `buscar_por_id`, `listar`, `atualizar`, `excluir`, `fechar`
5. Adicionar validações específicas em `utils/validacoes.py`
6. Ligar o CRUD da classe em `menu.py`
7. Testar localmente (`python main.py`) contra o banco da Aiven
8. Abrir o Pull Request e mover o card no Trello para "Revisão"

---

## ✅ Exemplo preenchido — Perfil

**Tabela SQL:** `perfis`
**Classe:** `Perfil`
**Comando do Git:**
```
git checkout -b "Feature/Issue-#1/Perfis"
```

**Código da Tabela do Banco de Dados:**
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

**Arquivos já criados nesta vertical** (sirva de referência ao preencher as próximas classes):
- `sistema_manutencao/models/perfil.py`
- `sistema_manutencao/repositories/perfil_repository.py`
- `sistema_manutencao/utils/validacoes.py` (`validar_nome_perfil`, `validar_campo_obrigatorio`)
- `sistema_manutencao/menu.py` (opções 1 a 5 do menu)

---

## 🗺️ Próximas classes (a partir dos requisitos do THAF)

Mapeamento dos requisitos funcionais/regras de negócio do documento
`Projeto_SA_THAF` para as próximas tabelas/classes a criar — use esta lista
para abrir os próximos cards no mesmo formato acima.

| # | Classe | Tabela SQL | Requisito(s) | Branch sugerida |
|---|--------|-----------|---------------|------------------|
| 1 | `Perfil` | `perfis` | RN-002 | `Feature/Issue-#1/Perfis` ✅ feito |
| 2 | `Usuario` | `usuarios` | RF06, RF07, RF08, RF09, RN-002, RN-003 | `Feature/Issue-#2/Usuarios` |
| 3 | `LogAuditoria` | `logs_auditoria` | RN-003 (IP, timestamp, resultado do login) | `Feature/Issue-#3/LogsAuditoria` |
| 4 | `Ativo` (máquina/equipamento) | `ativos` | RF01, RN-001, RN-004, RN-005, RN-006 | `Feature/Issue-#4/Ativos` |
| 5 | `OrdemServico` | `ordens_servico` | RF02, RN-007, RN-008 | `Feature/Issue-#5/OrdensServico` |
| 6 | `Peca` / `ItemEstoque` | `itens_estoque` | RF04, RN-009, RN-010 | `Feature/Issue-#6/Estoque` |
| 7 | `Ferramenta` | `ferramentas` | RN-011, RN-012 | `Feature/Issue-#7/Ferramentas` |
| 8 | `CronogramaPreventivo` | `cronograma_preventivo` | RF05 | `Feature/Issue-#8/CronogramaPreventivo` |
| 9 | `RiscoEpi` | `riscos_epis` | RN-013, RN-014 (NR-01) | `Feature/Issue-#9/RiscosEpis` |

> Observação: o RF03 (rastreamento de status dos técnicos) não é uma tabela
> nova — é um campo/consulta sobre `usuarios` (disponibilidade, carga de
> trabalho, estado de atendimento em tempo real).
