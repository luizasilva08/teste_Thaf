from dataclasses import dataclass
from datetime import datetime
from typing import Optional

STATUS_VALIDOS = ("Operando", "Manutenção", "Parado", "Crítico")


@dataclass
class Maquina:
    setor_id: int
    tag: str
    nome: str
    status_vivo: str = "Operando"
    id: Optional[int] = None
    ultima_manutencao: Optional[datetime] = None
