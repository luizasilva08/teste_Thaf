from dataclasses import dataclass
from typing import Optional

PERFIS_VALIDOS = ("coordenador", "gestor", "professor", "aluno", "representante")


@dataclass
class Perfil:
    nome: str
    descricao: Optional[str] = None
    id: Optional[int] = None
