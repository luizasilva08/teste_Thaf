from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class LogAuditoria:
    usuario_id: int
    acao: str
    endereco_ip: Optional[str] = None
    id: Optional[int] = None
    criado_em: Optional[datetime] = None
