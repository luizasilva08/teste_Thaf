from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Usuario:
    perfil_id: int
    nome: str
    email: str
    senha_hash: str
    turma_id: Optional[int] = None
    id: Optional[int] = None
    criado_em: Optional[datetime] = None
