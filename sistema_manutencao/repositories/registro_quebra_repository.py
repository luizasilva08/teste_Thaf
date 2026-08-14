from database.conexao import Conexao
from models.registro_quebra import RegistroQuebra

class RegistroQuebraRepository:
    """registros_quebra usa soft delete por HERANÇA (ver notas em
    usuario_repository.py) — usa "FROM ONLY registros_quebra".
    """

    def __init__(self):
        self.db = Conexao()

    def criar_registro(self, registro):
        return RegistroQuebra(
            id_quebra=registro[0],
            item_id=registro[1],
            usuario_id=registro[2],
            descricao_quebra=registro[3],
            foto_url=registro[4],
            criado_em=registro[5]
        )

    def salvar(self, registro_quebra):
        sql = """
        INSERT INTO registros_quebra
        (
            item_id,
            usuario_id,
            descricao_quebra,
            foto_url
        )
        VALUES
        (
            %s, %s, %s, %s
        )
        """
        valores = (
            registro_quebra.item_id,
            registro_quebra.usuario_id,
            registro_quebra.descricao_quebra,
            registro_quebra.foto_url
        )
        try:
            self.db.cursor.execute(sql, valores)
            self.db.commit()
            print("Registro de quebra cadastrado com sucesso!")

        except Exception as erro:
            self.db.rollback()
            print(f"Erro ao cadastrar registro de quebra. Erro: {erro}")

    def buscar_por_id(self, id_quebra):
        sql = """
        SELECT id_quebra, item_id, usuario_id, descricao_quebra, foto_url, criado_em
        FROM ONLY registros_quebra
        WHERE id_quebra = %s
        """
        try:
            self.db.cursor.execute(sql, (id_quebra,))
            registro = self.db.cursor.fetchone()

            if registro is None:
                return None

            return self.criar_registro(registro)

        except Exception as erro:
            print(f"Erro ao buscar registro de quebra pelo id. Erro: {erro}")
            return None

    def listar(self):
        sql = """
            SELECT id_quebra, item_id, usuario_id, descricao_quebra, foto_url, criado_em
            FROM ONLY registros_quebra
            ORDER BY criado_em DESC
        """
        try:
            self.db.cursor.execute(sql)
            registros = self.db.cursor.fetchall()
            quebras = []

            for registro in registros:
                quebras.append(self.criar_registro(registro))
            return quebras

        except Exception as erro:
            print(f"Erro ao listar registros de quebra: {erro}")
            return []

    def listar_por_item(self, item_id):
        sql = """
            SELECT id_quebra, item_id, usuario_id, descricao_quebra, foto_url, criado_em
            FROM ONLY registros_quebra
            WHERE item_id = %s
            ORDER BY criado_em DESC
        """
        try:
            self.db.cursor.execute(sql, (item_id,))
            registros = self.db.cursor.fetchall()
            quebras = []

            for registro in registros:
                quebras.append(self.criar_registro(registro))
            return quebras

        except Exception as erro:
            print(f"Erro ao listar registros de quebra por item: {erro}")
            return []

    def excluir(self, id_quebra):
        sql = """
            DELETE FROM registros_quebra
            WHERE id_quebra = %s
        """
        try:
            self.db.cursor.execute(sql, (id_quebra,))
            self.db.commit()

            if self.db.cursor.rowcount == 0:
                print("Registro de quebra não encontrado!")

            else:
                print("Registro de quebra excluído com sucesso!")

        except Exception as erro:
            self.db.rollback()
            print(f"Erro ao excluir registro de quebra: {erro}")

    def fechar(self):
        self.db.fechar()
