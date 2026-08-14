from dataclasses import dataclass
from datetime import datetime
from typing import Optional

PRIORIDADES_VALIDAS = ("Baixa", "Média", "Alta")
TIPOS_MANUTENCAO_VALIDOS = ("Corretiva", "Preventiva", "Preditiva")

# Transições permitidas no fluxo da S.S.
STATUS_VALIDOS = ("Aberta", "Em Análise", "Aguardando Peças", "Execução", "Validação", "Concluída")
TRANSICOES_PERMITIDAS = {
    "Aberta": {"Em Análise"},
    "Em Análise": {"Aguardando Peças", "Execução"},
    "Aguardando Peças": {"Execução"},
    "Execução": {"Validação"},
    "Validação": {"Concluída", "Execução"},
    "Concluída": set(),
}


@dataclass
class SolicitacaoServico:
    maquina_id: int
    solicitante_id: int
    descricao_problema: str
    responsavel_id: Optional[int] = None
    professor_validador_id: Optional[int] = None
    prioridade_ss: str = "Média"
    tipo_manutencao: str = "Corretiva"
    status: str = "Aberta"
    id: Optional[int] = None
    criado_em: Optional[datetime] = None
    atualizado_em: Optional[datetime] = None
