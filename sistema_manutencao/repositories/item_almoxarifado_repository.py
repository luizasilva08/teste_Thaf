from database.conexao import obter_conexao
from models.item_almoxarifado import ItemAlmoxarifado
from repositories.alerta_estoque_repository import AlertaEstoqueRepository
from repositories.base_repository import BaseRepository


class ItemAlmoxarifadoRepository(BaseRepository):
    tabela = "itens_almoxarifado"
    colunas = ("nome", "dimensao", "quantidade_atual", "estoque_minimo", "unidade_medida", "localizacao_gaveta")
    model_cls = ItemAlmoxarifado

    def _movimentar(self, id_: int, delta: int) -> ItemAlmoxarifado:
        sql = "UPDATE itens_almoxarifado SET quantidade_atual = quantidade_atual + %s WHERE id = %s"
        conn = obter_conexao()
        try:
            cursor = conn.cursor()
            cursor.execute(sql, (delta, id_))
            conn.commit()
            cursor.close()
        finally:
            conn.close()

        item = self.buscar_por_id(id_)
        if item and item.quantidade_atual < item.estoque_minimo:
            AlertaEstoqueRepository().criar_se_nao_existir(
                item_id=item.id,
                mensagem=f"Estoque de '{item.nome}' abaixo do mínimo ({item.quantidade_atual}/{item.estoque_minimo}).",
            )
        return item

    def dar_entrada(self, id_: int, quantidade: int) -> ItemAlmoxarifado:
        return self._movimentar(id_, abs(quantidade))

    def dar_baixa(self, id_: int, quantidade: int) -> ItemAlmoxarifado:
        return self._movimentar(id_, -abs(quantidade))

    def listar_abaixo_do_minimo(self):
        sql = "SELECT * FROM itens_almoxarifado WHERE quantidade_atual < estoque_minimo ORDER BY nome"
        conn = obter_conexao()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(sql)
            linhas = cursor.fetchall()
            cursor.close()
            return [self._linha_para_model(linha) for linha in linhas]
        finally:
            conn.close()
