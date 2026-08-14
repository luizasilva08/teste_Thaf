from database.conexao import obter_conexao
from models.usuario import Usuario
from repositories.base_repository import BaseRepository


class UsuarioRepository(BaseRepository):
    tabela = "usuarios"
    colunas = ("perfil_id", "turma_id", "nome", "email", "senha_hash")
    model_cls = Usuario

    def buscar_por_email(self, email: str):
        conn = obter_conexao()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM usuarios WHERE email = %s", (email,))
            linha = cursor.fetchone()
            cursor.close()
            return self._linha_para_model(linha) if linha else None
        finally:
            conn.close()

    def listar_por_turma(self, turma_id: int):
        return self.listar(filtros={"turma_id": turma_id})

    def listar_por_perfil(self, perfil_id: int):
        return self.listar(filtros={"perfil_id": perfil_id})
