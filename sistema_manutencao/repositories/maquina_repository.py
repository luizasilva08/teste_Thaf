from database.conexao import Conexao
from models.maquina import Maquina

class MaquinaRepository:
    def __init__(self):
        self.db = Conexao()

    def criar_maquina(self, registro):
        return Maquina(
            id_maquina=registro[0],
            setor_id=registro[1],
            tag=registro[2],
            nome=registro[3],
            status_vivo=registro[4],
            ultima_manutencao=registro[5]
        )

    def salvar(self, maquina):
        sql = """
        INSERT INTO maquinas
        (
            setor_id,
            tag,
            nome,
            status_vivo
        )
        VALUES
        (
            %s, %s, %s, %s
        )
        """
        valores = (
            maquina.setor_id,
            maquina.tag,
            maquina.nome,
            maquina.status_vivo
        )
        try:
            self.db.cursor.execute(sql, valores)
            self.db.commit()
            print("Máquina cadastrada com sucesso!")

        except Exception as erro:
            self.db.rollback()
            print(f"Erro ao cadastrar máquina. Erro: {erro}")

    def buscar_por_id(self, id_maquina):
        sql = """
        SELECT *
        FROM maquinas
        WHERE id = %s
        """
        try:
            self.db.cursor.execute(sql, (id_maquina,))
            registro = self.db.cursor.fetchone()

            if registro is None:
                return None

            return self.criar_maquina(registro)

        except Exception as erro:
            print(f"Erro ao buscar máquina pelo id. Erro: {erro}")
            return None

    def listar(self):
        sql = """
            SELECT *
            FROM maquinas
            ORDER BY tag
        """
        try:
            self.db.cursor.execute(sql)
            registros = self.db.cursor.fetchall()
            maquinas = []

            for registro in registros:
                maquinas.append(self.criar_maquina(registro))
            return maquinas

        except Exception as erro:
            print(f"Erro ao listar máquinas: {erro}")
            return []

    def listar_por_setor(self, setor_id):
        sql = """
            SELECT *
            FROM maquinas
            WHERE setor_id = %s
            ORDER BY tag
        """
        try:
            self.db.cursor.execute(sql, (setor_id,))
            registros = self.db.cursor.fetchall()
            maquinas = []

            for registro in registros:
                maquinas.append(self.criar_maquina(registro))
            return maquinas

        except Exception as erro:
            print(f"Erro ao listar máquinas por setor: {erro}")
            return []

    def listar_por_status(self, status_vivo):
        sql = """
            SELECT *
            FROM maquinas
            WHERE status_vivo = %s
            ORDER BY tag
        """
        try:
            self.db.cursor.execute(sql, (status_vivo,))
            registros = self.db.cursor.fetchall()
            maquinas = []

            for registro in registros:
                maquinas.append(self.criar_maquina(registro))
            return maquinas

        except Exception as erro:
            print(f"Erro ao listar máquinas por status: {erro}")
            return []

    def atualizar(self, maquina):
        sql = """UPDATE maquinas
        SET
            setor_id = %s,
            tag = %s,
            nome = %s,
            status_vivo = %s
        WHERE id = %s
        """
        valores = (
            maquina.setor_id,
            maquina.tag,
            maquina.nome,
            maquina.status_vivo,
            maquina.id_maquina
        )
        try:
            self.db.cursor.execute(sql, valores)
            self.db.commit()
            if self.db.cursor.rowcount == 0:
                print("Máquina não encontrada!")

            else:
                print("Máquina atualizada!")

        except Exception as erro:
            self.db.rollback()
            print(f"Erro ao atualizar máquina: {erro}")

    def atualizar_status(self, id_maquina, status_vivo):
        sql = """
            UPDATE maquinas
            SET status_vivo = %s
            WHERE id = %s
        """
        try:
            self.db.cursor.execute(sql, (status_vivo, id_maquina))
            self.db.commit()

            if self.db.cursor.rowcount == 0:
                print("Máquina não encontrada!")

            else:
                print("Status atualizado!")

        except Exception as erro:
            self.db.rollback()
            print(f"Erro ao atualizar status da máquina: {erro}")

    def registrar_manutencao_concluida(self, id_maquina):
        sql = """
            UPDATE maquinas
            SET status_vivo = 'Operando', ultima_manutencao = NOW()
            WHERE id = %s
        """
        try:
            self.db.cursor.execute(sql, (id_maquina,))
            self.db.commit()

            if self.db.cursor.rowcount == 0:
                print("Máquina não encontrada!")

            else:
                print("Manutenção registrada — máquina voltou a 'Operando'.")

        except Exception as erro:
            self.db.rollback()
            print(f"Erro ao registrar manutenção concluída: {erro}")

    def excluir(self, id_maquina):
        sql = """
            DELETE FROM maquinas
            WHERE id = %s
        """
        try:
            self.db.cursor.execute(sql, (id_maquina,))
            self.db.commit()

            if self.db.cursor.rowcount == 0:
                print("Máquina não encontrada!")

            else:
                print("Máquina excluída com sucesso!")

        except Exception as erro:
            self.db.rollback()
            print(f"Erro ao excluir máquina: {erro}")

    def fechar(self):
        self.db.fechar()
