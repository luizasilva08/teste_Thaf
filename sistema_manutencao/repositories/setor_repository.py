from models.setor import Setor
from repositories.base_repository import BaseRepository


class SetorRepository(BaseRepository):
    tabela = "setores"
    colunas = ("nome", "descricao")
    model_cls = Setor
