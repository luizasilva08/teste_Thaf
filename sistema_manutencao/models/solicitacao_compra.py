from dataclasses import dataclass
from datetime import datetime
from typing import Optional

STATUS_VALIDOS = ("Não Visualizado", "Em Análise", "Pedido em Andamento", "Entregue")


@dataclass
class SolicitacaoCompra:
    solicitante_id: int
    professor_responsavel_id: int
    especificacao_tecnica: str
    justificativa: str
    turma_id: Optional[int] = None
    maquina_id: Optional[int] = None
    status: str = "Não Visualizado"
    quantidade: int = 1
    sap: Optional[str] = None
    patrimonio: Optional[str] = None
    equipamento: Optional[str] = None
    conjunto_mecanico: Optional[str] = None
    arquivos: Optional[str] = None
    id: Optional[int] = None
    criado_em: Optional[datetime] = None
