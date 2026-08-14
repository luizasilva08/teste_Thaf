from dataclasses import dataclass
from datetime import date, datetime, time
from typing import Optional

TIPOS_MANUTENCAO_VALIDOS = ("Corretiva", "Preventiva", "Preditiva", "Melhoria")
CRITICIDADES_VALIDAS = ("Baixa", "Média", "Alta", "Crítica")


@dataclass
class OrdemServico:
    solicitacao_id: int
    maquina_id: int
    tipo_manutencao: str
    criticidade: str
    descricao_execucao: str
    data_execucao: date
    hora_inicio: time
    hora_fim: time
    turma_id: Optional[int] = None
    pecas_usadas: Optional[str] = None
    quantidade_pessoas: int = 1
    id: Optional[int] = None
    criado_em: Optional[datetime] = None
