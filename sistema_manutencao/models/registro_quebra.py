from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class RegistroQuebra:
    item_id: int
    usuario_id: int
    descricao: str
    foto_url: Optional[str] = None
    id: Optional[int] = None
    criado_em: Optional[datetime] = None
