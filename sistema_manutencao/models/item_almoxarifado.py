from dataclasses import dataclass
from typing import Optional


@dataclass
class ItemAlmoxarifado:
    nome: str
    quantidade_atual: int = 0
    estoque_minimo: int = 1
    unidade_medida: str = "UN"
    dimensao: Optional[str] = None
    localizacao_gaveta: Optional[str] = None
    id: Optional[int] = None
