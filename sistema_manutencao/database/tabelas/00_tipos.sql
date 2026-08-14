-- Tipos ENUM (equivalentes aos ENUM inline do MySQL). Compartilhado entre
-- várias tabelas — só edite se estiver criando um enum novo, adicionando no
-- final do arquivo.

CREATE TYPE status_maquina_enum      AS ENUM ('Operando','Manutenção','Parado','Crítico');
CREATE TYPE status_alerta_enum       AS ENUM ('Pendente','Resolvido');
CREATE TYPE prioridade_ss_enum       AS ENUM ('Baixa','Média','Alta');
CREATE TYPE tipo_manutencao_ss_enum  AS ENUM ('Corretiva','Preventiva','Preditiva');
CREATE TYPE status_ss_enum           AS ENUM ('Aberta','Em Análise','Aguardando Peças','Execução','Validação','Concluída');
CREATE TYPE tipo_manutencao_os_enum  AS ENUM ('Corretiva','Preventiva','Preditiva','Melhoria');
CREATE TYPE criticidade_os_enum      AS ENUM ('Baixa','Média','Alta','Crítica');
CREATE TYPE status_compra_enum       AS ENUM ('Não Visualizado','Em Análise','Pedido em Andamento','Entregue');
CREATE TYPE frequencia_cal_enum      AS ENUM ('Diária','Semanal','Quinzenal','Mensal','Semestral','Anual');
CREATE TYPE status_cal_enum          AS ENUM ('Agendada','Em Execução','Concluída','Atrasada','Cancelada');
