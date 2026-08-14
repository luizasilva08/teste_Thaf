from dataclasses import dataclass
from datetime import datetime
from typing import Optional

STATUS_VALIDOS = ("Pendente", "Resolvido")


@dataclass
class AlertaEstoque:
    item_id: int
    mensagem: str
    status: str = "Pendente"
    id: Optional[int] = None
    criado_em: Optional[datetime] = None
