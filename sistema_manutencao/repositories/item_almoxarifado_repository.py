from database.conexao import Conexao
from models.item_almoxarifado import ItemAlmoxarifado

class ItemAlmoxarifadoRepository:
    """itens_almoxarifado usa soft delete por HERANÇA (ver notas em
    usuario_repository.py) — usa "FROM ONLY itens_almoxarifado".
    """

    def __init__(self):
        self.db = Conexao()

    def criar_item(self, registro):
        return ItemAlmoxarifado(
            id_ferramenta=registro[0],
            nome_ferramenta=registro[1],
            dimensao_ferramenta=registro[2],
            quantidade_atual=registro[3],
            estoque_minimo=registro[4],
            unidade_medida=registro[5],
            localizacao_gaveta=registro[6]
        )

    def salvar(self, item):
        sql = """
        INSERT INTO itens_almoxarifado
        (
            nome_ferramenta,
            dimensao_ferramenta,
            quantidade_atual,
            estoque_minimo,
            unidade_medida,
            localizacao_gaveta
        )
        VALUES
        (
            %s, %s, %s, %s, %s, %s
        )
        """
        valores = (
            item.nome_ferramenta,
            item.dimensao_ferramenta,
            item.quantidade_atual,
            item.estoque_minimo,
            item.unidade_medida,
            item.localizacao_gaveta
        )
        try:
            self.db.cursor.execute(sql, valores)
            self.db.commit()
            print("Item cadastrado com sucesso!")

        except Exception as erro:
            self.db.rollback()
            print(f"Erro ao cadastrar item. Erro: {erro}")

    def buscar_por_id(self, id_ferramenta):
        sql = """
        SELECT id_ferramenta, nome_ferramenta, dimensao_ferramenta, quantidade_atual,
               estoque_minimo, unidade_medida, localizacao_gaveta
        FROM ONLY itens_almoxarifado
        WHERE id_ferramenta = %s
        """
        try:
            self.db.cursor.execute(sql, (id_ferramenta,))
            registro = self.db.cursor.fetchone()

            if registro is None:
                return None

            return self.criar_item(registro)

        except Exception as erro:
            print(f"Erro ao buscar item pelo id. Erro: {erro}")
            return None

    def listar(self):
        sql = """
            SELECT id_ferramenta, nome_ferramenta, dimensao_ferramenta, quantidade_atual,
                   estoque_minimo, unidade_medida, localizacao_gaveta
            FROM ONLY itens_almoxarifado
            ORDER BY nome_ferramenta
        """
        try:
            self.db.cursor.execute(sql)
            registros = self.db.cursor.fetchall()
            itens = []

            for registro in registros:
                itens.append(self.criar_item(registro))
            return itens

        except Exception as erro:
            print(f"Erro ao listar itens: {erro}")
            return []

    def listar_abaixo_do_minimo(self):
        sql = """
            SELECT id_ferramenta, nome_ferramenta, dimensao_ferramenta, quantidade_atual,
                   estoque_minimo, unidade_medida, localizacao_gaveta
            FROM ONLY itens_almoxarifado
            WHERE quantidade_atual < estoque_minimo
            ORDER BY nome_ferramenta
        """
        try:
            self.db.cursor.execute(sql)
            registros = self.db.cursor.fetchall()
            itens = []

            for registro in registros:
                itens.append(self.criar_item(registro))
            return itens

        except Exception as erro:
            print(f"Erro ao listar itens abaixo do mínimo: {erro}")
            return []

    def atualizar(self, item):
        sql = """UPDATE itens_almoxarifado
        SET
            nome_ferramenta = %s,
            dimensao_ferramenta = %s,
            estoque_minimo = %s,
            unidade_medida = %s,
            localizacao_gaveta = %s
        WHERE id_ferramenta = %s
        """
        valores = (
            item.nome_ferramenta,
            item.dimensao_ferramenta,
            item.estoque_minimo,
            item.unidade_medida,
            item.localizacao_gaveta,
            item.id_ferramenta
        )
        try:
            self.db.cursor.execute(sql, valores)
            self.db.commit()
            if self.db.cursor.rowcount == 0:
                print("Item não encontrado!")

            else:
                print("Item atualizado!")

        except Exception as erro:
            self.db.rollback()
            print(f"Erro ao atualizar item: {erro}")

    def dar_entrada(self, id_ferramenta, quantidade):
        return self._movimentar(id_ferramenta, abs(quantidade))

    def dar_baixa(self, id_ferramenta, quantidade):
        item = self._movimentar(id_ferramenta, -abs(quantidade))

        if item is not None and item.quantidade_atual < item.estoque_minimo:
            from repositories.alerta_estoque_repository import AlertaEstoqueRepository
            alertas = AlertaEstoqueRepository()
            alertas.criar_se_nao_existir(
                item_id=item.id_ferramenta,
                mensagem=f"Estoque de '{item.nome_ferramenta}' abaixo do mínimo ({item.quantidade_atual}/{item.estoque_minimo})."
            )
            alertas.fechar()

        return item

    def _movimentar(self, id_ferramenta, delta):
        sql = """
            UPDATE itens_almoxarifado
            SET quantidade_atual = quantidade_atual + %s
            WHERE id_ferramenta = %s
        """
        try:
            self.db.cursor.execute(sql, (delta, id_ferramenta))
            self.db.commit()

            if self.db.cursor.rowcount == 0:
                print("Item não encontrado!")
                return None

            print("Estoque atualizado!")
            return self.buscar_por_id(id_ferramenta)

        except Exception as erro:
            self.db.rollback()
            print(f"Erro ao movimentar estoque: {erro}")
            return None

    def excluir(self, id_ferramenta):
        sql = """
            DELETE FROM itens_almoxarifado
            WHERE id_ferramenta = %s
        """
        try:
            self.db.cursor.execute(sql, (id_ferramenta,))
            self.db.commit()

            if self.db.cursor.rowcount == 0:
                print("Item não encontrado!")

            else:
                print("Item excluído com sucesso!")

        except Exception as erro:
            self.db.rollback()
            print(f"Erro ao excluir item: {erro}")

    def fechar(self):
        self.db.fechar()
