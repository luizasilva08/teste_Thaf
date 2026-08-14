from models.registro_quebra import RegistroQuebra
from repositories.base_repository import BaseRepository


class RegistroQuebraRepository(BaseRepository):
    tabela = "registros_quebra"
    colunas = ("item_id", "usuario_id", "descricao", "foto_url")
    model_cls = RegistroQuebra

    def listar_por_item(self, item_id: int):
        return self.listar(filtros={"item_id": item_id})

    def listar_por_usuario(self, usuario_id: int):
        return self.listar(filtros={"usuario_id": usuario_id})
