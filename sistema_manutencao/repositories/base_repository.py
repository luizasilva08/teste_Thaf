from database.conexao import obter_conexao


class BaseRepository:
    """CRUD genérico sobre uma tabela. Subclasses definem tabela/colunas/model."""

    tabela: str = ""
    colunas: tuple = ()  # colunas graváveis, sem 'id'
    model_cls = None

    def _linha_para_model(self, linha: dict):
        return self.model_cls(**linha)

    def criar(self, entidade) -> int:
        campos = ", ".join(self.colunas)
        placeholders = ", ".join(["%s"] * len(self.colunas))
        valores = tuple(getattr(entidade, coluna) for coluna in self.colunas)

        sql = f"INSERT INTO {self.tabela} ({campos}) VALUES ({placeholders})"

        conn = obter_conexao()
        try:
            cursor = conn.cursor()
            cursor.execute(sql, valores)
            conn.commit()
            novo_id = cursor.lastrowid
            cursor.close()
            return novo_id
        finally:
            conn.close()

    def buscar_por_id(self, id_: int):
        sql = f"SELECT * FROM {self.tabela} WHERE id = %s"
        conn = obter_conexao()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(sql, (id_,))
            linha = cursor.fetchone()
            cursor.close()
            return self._linha_para_model(linha) if linha else None
        finally:
            conn.close()

    def listar(self, filtros: dict = None, ordenar_por: str = "id"):
        sql = f"SELECT * FROM {self.tabela}"
        valores = ()
        if filtros:
            condicoes = " AND ".join(f"{campo} = %s" for campo in filtros)
            sql += f" WHERE {condicoes}"
            valores = tuple(filtros.values())
        sql += f" ORDER BY {ordenar_por}"

        conn = obter_conexao()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(sql, valores)
            linhas = cursor.fetchall()
            cursor.close()
            return [self._linha_para_model(linha) for linha in linhas]
        finally:
            conn.close()

    def atualizar(self, id_: int, entidade) -> bool:
        campos = ", ".join(f"{coluna} = %s" for coluna in self.colunas)
        valores = tuple(getattr(entidade, coluna) for coluna in self.colunas) + (id_,)

        sql = f"UPDATE {self.tabela} SET {campos} WHERE id = %s"

        conn = obter_conexao()
        try:
            cursor = conn.cursor()
            cursor.execute(sql, valores)
            conn.commit()
            afetadas = cursor.rowcount
            cursor.close()
            return afetadas > 0
        finally:
            conn.close()

    def excluir(self, id_: int) -> bool:
        sql = f"DELETE FROM {self.tabela} WHERE id = %s"
        conn = obter_conexao()
        try:
            cursor = conn.cursor()
            cursor.execute(sql, (id_,))
            conn.commit()
            afetadas = cursor.rowcount
            cursor.close()
            return afetadas > 0
        finally:
            conn.close()
