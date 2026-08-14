from dataclasses import dataclass
from typing import Optional


@dataclass
class Turma:
    codigo: str
    periodo: str
    id: Optional[int] = None
