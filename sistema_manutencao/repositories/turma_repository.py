from models.turma import Turma
from repositories.base_repository import BaseRepository


class TurmaRepository(BaseRepository):
    tabela = "turmas"
    colunas = ("codigo", "periodo")
    model_cls = Turma
