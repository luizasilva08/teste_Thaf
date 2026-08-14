from models.perfil import Perfil
from repositories.base_repository import BaseRepository


class PerfilRepository(BaseRepository):
    tabela = "perfis"
    colunas = ("nome", "descricao")
    model_cls = Perfil
