from database.conexao import Conexao
from models.usuario import Usuario

class UsuarioSoftDelete:
    """Operações sobre usuários EXCLUÍDOS.

    usuarios usa soft delete por HERANÇA: o DELETE do UsuarioRepository
    move a linha inteira para usuarios_deletados (trigger
    trg_soft_delete_usuarios). Restaurar significa inserir a linha de
    volta em usuarios (preservando o id_usuario original, via
    OVERRIDING SYSTEM VALUE porque a coluna é IDENTITY) e apagar de
    usuarios_deletados.
    """

    def __init__(self):
        self.db = Conexao()

    def criar_usuario(self, registro):
        return Usuario(
            id_usuario=registro[0],
            perfil_id=registro[1],
            turma_id=registro[2],
            nome_usuario=registro[3],
            email_usuario=registro[4],
            senha_hash=registro[5],
            criado_em=registro[6],
            deleted_at=registro[7]
        )

    def listar_excluidos(self):
        sql = """
            SELECT id_usuario, perfil_id, turma_id, nome_usuario, email_usuario,
                   senha_hash, criado_em, deleted_at
            FROM usuarios_deletados
            ORDER BY deleted_at DESC
        """
        try:
            self.db.cursor.execute(sql)
            registros = self.db.cursor.fetchall()
            usuarios = []

            for registro in registros:
                usuarios.append(self.criar_usuario(registro))
            return usuarios

        except Exception as erro:
            print(f"Erro ao listar usuários excluídos: {erro}")
            return []

    def buscar_excluido_por_id(self, id_usuario):
        sql = """
            SELECT id_usuario, perfil_id, turma_id, nome_usuario, email_usuario,
                   senha_hash, criado_em, deleted_at
            FROM usuarios_deletados
            WHERE id_usuario = %s
        """
        try:
            self.db.cursor.execute(sql, (id_usuario,))
            registro = self.db.cursor.fetchone()

            if registro is None:
                return None

            return self.criar_usuario(registro)

        except Exception as erro:
            print(f"Erro ao buscar usuário excluído pelo id. Erro: {erro}")
            return None

    def restaurar(self, id_usuario):
        usuario = self.buscar_excluido_por_id(id_usuario)
        if usuario is None:
            print("Usuário excluído não encontrado!")
            return

        sql_inserir = """
            INSERT INTO usuarios
            (id_usuario, perfil_id, turma_id, nome_usuario, email_usuario, senha_hash, criado_em)
            OVERRIDING SYSTEM VALUE
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        sql_apagar = """
            DELETE FROM usuarios_deletados
            WHERE id_usuario = %s
        """
        try:
            self.db.cursor.execute(sql_inserir, (
                usuario.id_usuario, usuario.perfil_id, usuario.turma_id,
                usuario.nome_usuario, usuario.email_usuario, usuario.senha_hash, usuario.criado_em
            ))
            self.db.cursor.execute(sql_apagar, (id_usuario,))
            self.db.commit()
            print("Usuário restaurado com sucesso!")

        except Exception as erro:
            self.db.rollback()
            print(f"Erro ao restaurar usuário: {erro}")

    def fechar(self):
        self.db.fechar()
