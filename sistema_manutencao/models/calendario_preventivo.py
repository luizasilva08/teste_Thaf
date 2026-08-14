from dataclasses import dataclass
from datetime import date, datetime
from typing import Optional

FREQUENCIAS_VALIDAS = ("Diária", "Semanal", "Quinzenal", "Mensal", "Semestral", "Anual")
STATUS_VALIDOS = ("Agendada", "Em Execução", "Concluída", "Atrasada", "Cancelada")

DIAS_POR_FREQUENCIA = {
    "Diária": 1,
    "Semanal": 7,
    "Quinzenal": 15,
    "Mensal": 30,
    "Semestral": 182,
    "Anual": 365,
}


@dataclass
class CalendarioPreventivo:
    maquina_id: int
    titulo: str
    frequencia: str
    data_proxima_execucao: date
    turma_id: Optional[int] = None
    responsavel_id: Optional[int] = None
    descricao: Optional[str] = None
    status: str = "Agendada"
    id: Optional[int] = None
    criado_em: Optional[datetime] = None
