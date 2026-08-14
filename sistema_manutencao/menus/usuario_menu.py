from models.usuario import Usuario
from repositories.usuario_repository import UsuarioRepository
from utils.usuario_validacoes import (
    gerar_hash_senha,
    validar_email_usuario,
    validar_nome_usuario,
    validar_senha_usuario,
)

from menus.gradiente import gradiente_texto


class MenuUsuario:

    # Roxo industrial: roxo escuro -> roxo -> lilás claro
    ROXO_ESCURO = (35, 15, 45)
    ROXO = (110, 60, 150)
    LILAS_CLARO = (210, 180, 230)

    def __init__(self):
        self.repository = UsuarioRepository()

    # submenu
    def exibir(self):
        while True:
            print()
            print(gradiente_texto("=" * 60, self.ROXO_ESCURO, self.LILAS_CLARO))
            print(gradiente_texto("CTW MANUTENÇÃO - USUÁRIOS", self.ROXO, self.LILAS_CLARO))
            print(gradiente_texto("=" * 60, self.LILAS_CLARO, self.ROXO_ESCURO))
            print(gradiente_texto("1 - Cadastrar Usuário", self.ROXO_ESCURO, self.ROXO))
            print(gradiente_texto("2 - Buscar Usuário", self.ROXO_ESCURO, self.ROXO))
            print(gradiente_texto("3 - Listar Usuários", self.ROXO, self.LILAS_CLARO))
            print(gradiente_texto("4 - Listar Usuários por Perfil", self.ROXO, self.LILAS_CLARO))
            print(gradiente_texto("5 - Atualizar Usuário", self.ROXO, self.LILAS_CLARO))
            print(gradiente_texto("6 - Excluir Usuário", self.ROXO_ESCURO, self.LILAS_CLARO))
            print(gradiente_texto("0 - Sair", self.ROXO_ESCURO, self.ROXO))
            print(gradiente_texto("=" * 60, self.LILAS_CLARO, self.ROXO_ESCURO))

            opcao = input(gradiente_texto("Escolha uma opção: ", self.LILAS_CLARO, self.ROXO_ESCURO))

            if opcao == "1":
                self.cadastrar_usuario()

            elif opcao == "2":
                self.buscar_usuario()

            elif opcao == "3":
                self.listar_usuario()

            elif opcao == "4":
                self.listar_usuario_por_perfil()

            elif opcao == "5":
                self.atualizar_usuario()

            elif opcao == "6":
                self.excluir_usuario()

            elif opcao == "0":
                self.repository.fechar()
                print()
                print(gradiente_texto("Voltando ao menu principal...", self.ROXO_ESCURO, self.ROXO))
                break

            else:
                print()
                print(gradiente_texto("Opção inválida!", self.LILAS_CLARO, self.ROXO_ESCURO))

    def cadastrar_usuario(self):
        print()
        print(gradiente_texto("=" * 60, self.ROXO_ESCURO, self.LILAS_CLARO))
        print(gradiente_texto("CADASTRO DE USUÁRIO", self.ROXO, self.LILAS_CLARO))
        print(gradiente_texto("=" * 60, self.LILAS_CLARO, self.ROXO_ESCURO))

        try:
            nome_usuario = validar_nome_usuario(
                input(gradiente_texto("Nome: ", self.ROXO_ESCURO, self.ROXO))
            )
            email_usuario = validar_email_usuario(
                input(gradiente_texto("E-mail: ", self.ROXO_ESCURO, self.ROXO))
            )
            senha = validar_senha_usuario(
                input(gradiente_texto("Senha (mín. 6 caracteres): ", self.ROXO, self.LILAS_CLARO))
            )
            perfil_id = int(
                input(gradiente_texto("Código (id) do perfil: ", self.ROXO, self.LILAS_CLARO))
            )
            turma_id_texto = input(
                gradiente_texto("Código (id) da turma (ENTER se não houver): ", self.LILAS_CLARO, self.ROXO_ESCURO)
            )
            turma_id = int(turma_id_texto) if turma_id_texto.strip() else None

        except ValueError as erro:
            print()
            print(gradiente_texto(f"Erro: {erro}", self.LILAS_CLARO, self.ROXO_ESCURO))
            input("\nPressione ENTER para continuar...")
            return

        usuario = Usuario(
            perfil_id=perfil_id,
            turma_id=turma_id,
            nome_usuario=nome_usuario,
            email_usuario=email_usuario,
            senha_hash=gerar_hash_senha(senha)
        )
        self.repository.salvar(usuario)
        print()
        input("Pressione ENTER para continuar...")

    def buscar_usuario(self):
        print()
        print(gradiente_texto("=" * 60, self.ROXO_ESCURO, self.LILAS_CLARO))
        print(gradiente_texto("BUSCAR USUÁRIO", self.ROXO, self.LILAS_CLARO))
        print(gradiente_texto("=" * 60, self.LILAS_CLARO, self.ROXO_ESCURO))

        try:
            id_usuario = int(
                input(gradiente_texto("Código do usuário: ", self.ROXO_ESCURO, self.ROXO))
            )

        except ValueError:
            print()
            print("Código inválido.")
            input("\nPressione ENTER para continuar...")
            return

        usuario = self.repository.buscar_por_id(id_usuario)
        print()

        if usuario is None:
            print("Usuário não encontrado.")

        else:
            print(gradiente_texto(f"Código......: {usuario.id_usuario}", self.ROXO_ESCURO, self.ROXO))
            print(gradiente_texto(f"Nome........: {usuario.nome_usuario}", self.ROXO, self.LILAS_CLARO))
            print(gradiente_texto(f"E-mail......: {usuario.email_usuario}", self.LILAS_CLARO, self.ROXO_ESCURO))
            print(gradiente_texto(f"Perfil (id).: {usuario.perfil_id}", self.ROXO_ESCURO, self.ROXO))
            print(gradiente_texto(f"Turma (id)..: {usuario.turma_id}", self.ROXO, self.LILAS_CLARO))

        print()
        input("Pressione ENTER para continuar...")

    def listar_usuario(self):
        print()
        print(gradiente_texto("=" * 60, self.ROXO_ESCURO, self.LILAS_CLARO))
        print(gradiente_texto("LISTA DE USUÁRIOS", self.ROXO, self.LILAS_CLARO))
        print(gradiente_texto("=" * 60, self.LILAS_CLARO, self.ROXO_ESCURO))
        self._imprimir_lista(self.repository.listar())

    def listar_usuario_por_perfil(self):
        print()
        print(gradiente_texto("=" * 60, self.ROXO_ESCURO, self.LILAS_CLARO))
        print(gradiente_texto("USUÁRIOS POR PERFIL", self.ROXO, self.LILAS_CLARO))
        print(gradiente_texto("=" * 60, self.LILAS_CLARO, self.ROXO_ESCURO))

        try:
            perfil_id = int(
                input(gradiente_texto("Código (id) do perfil: ", self.ROXO_ESCURO, self.ROXO))
            )

        except ValueError:
            print()
            print("Código inválido.")
            input("\nPressione ENTER para continuar...")
            return

        self._imprimir_lista(self.repository.listar_por_perfil(perfil_id))

    def _imprimir_lista(self, usuarios):
        if not usuarios:
            print()
            print("Nenhum usuário encontrado.")
            print()
            input("Pressione ENTER para continuar...")
            return

        print(
            gradiente_texto(
                f"{'ID':<5}{'Nome':<25}{'E-mail':<30}{'Perfil':<8}",
                self.ROXO_ESCURO, self.LILAS_CLARO
            )
        )
        print(gradiente_texto("-" * 60, self.LILAS_CLARO, self.ROXO_ESCURO))

        for usuario in usuarios:
            print(
                gradiente_texto(
                    f"{usuario.id_usuario:<5}{usuario.nome_usuario:<25}{usuario.email_usuario:<30}{usuario.perfil_id:<8}",
                    self.ROXO, self.LILAS_CLARO
                )
            )

        print()
        print(gradiente_texto(f"Total de usuários: {len(usuarios)}", self.ROXO, self.LILAS_CLARO))
        print()
        input("Pressione ENTER para continuar...")

    def atualizar_usuario(self):
        print()
        print(gradiente_texto("=" * 60, self.ROXO_ESCURO, self.LILAS_CLARO))
        print(gradiente_texto("ATUALIZAÇÃO DE USUÁRIO", self.ROXO, self.LILAS_CLARO))
        print(gradiente_texto("=" * 60, self.LILAS_CLARO, self.ROXO_ESCURO))

        try:
            id_usuario = int(
                input(gradiente_texto("Código do usuário: ", self.ROXO_ESCURO, self.ROXO))
            )

        except ValueError:
            print()
            print("Código inválido.")
            input("\nPressione ENTER para continuar...")
            return

        usuario = self.repository.buscar_por_id(id_usuario)

        if usuario is None:
            print()
            print("Usuário não encontrado.")
            input("\nPressione ENTER para continuar...")
            return

        print()
        print(gradiente_texto("Pressione ENTER para manter o valor atual.", self.ROXO, self.LILAS_CLARO))
        print()

        nome_usuario = input(
            gradiente_texto(f"Nome [{usuario.nome_usuario}]: ", self.ROXO_ESCURO, self.ROXO)
        )
        if nome_usuario:
            try:
                usuario.nome_usuario = validar_nome_usuario(nome_usuario)
            except ValueError as erro:
                print(gradiente_texto(f"Erro: {erro}", self.LILAS_CLARO, self.ROXO_ESCURO))
                input("\nPressione ENTER para continuar...")
                return

        email_usuario = input(
            gradiente_texto(f"E-mail [{usuario.email_usuario}]: ", self.ROXO, self.LILAS_CLARO)
        )
        if email_usuario:
            try:
                usuario.email_usuario = validar_email_usuario(email_usuario)
            except ValueError as erro:
                print(gradiente_texto(f"Erro: {erro}", self.LILAS_CLARO, self.ROXO_ESCURO))
                input("\nPressione ENTER para continuar...")
                return

        senha = input(
            gradiente_texto("Nova senha (ENTER para manter a atual): ", self.LILAS_CLARO, self.ROXO_ESCURO)
        )
        if senha:
            try:
                usuario.senha_hash = gerar_hash_senha(validar_senha_usuario(senha))
            except ValueError as erro:
                print(gradiente_texto(f"Erro: {erro}", self.LILAS_CLARO, self.ROXO_ESCURO))
                input("\nPressione ENTER para continuar...")
                return

        perfil_id = input(
            gradiente_texto(f"Código (id) do perfil [{usuario.perfil_id}]: ", self.ROXO_ESCURO, self.ROXO)
        )
        if perfil_id:
            usuario.perfil_id = int(perfil_id)

        self.repository.atualizar(usuario)
        print()
        input("Pressione ENTER para continuar...")

    def excluir_usuario(self):
        print()
        print(gradiente_texto("=" * 60, self.ROXO_ESCURO, self.LILAS_CLARO))
        print(gradiente_texto("EXCLUSÃO DE USUÁRIO", self.ROXO, self.LILAS_CLARO))
        print(gradiente_texto("=" * 60, self.LILAS_CLARO, self.ROXO_ESCURO))

        try:
            id_usuario = int(
                input(gradiente_texto("Código do usuário: ", self.ROXO_ESCURO, self.ROXO))
            )

        except ValueError:
            print()
            print("Código inválido.")
            input("\nPressione ENTER para continuar...")
            return

        usuario = self.repository.buscar_por_id(id_usuario)

        if usuario is None:
            print()
            print("Usuário não encontrado.")
            input("\nPressione ENTER para continuar...")
            return

        print()
        print(gradiente_texto("Usuário localizado", self.ROXO, self.LILAS_CLARO))
        print(gradiente_texto("-" * 60, self.LILAS_CLARO, self.ROXO_ESCURO))
        print(gradiente_texto(f"Código.....: {usuario.id_usuario}", self.ROXO_ESCURO, self.ROXO))
        print(gradiente_texto(f"Nome.......: {usuario.nome_usuario}", self.ROXO, self.LILAS_CLARO))
        print()

        resposta = input(
            gradiente_texto("Deseja realmente excluir este usuário? (S/N): ", self.LILAS_CLARO, self.ROXO_ESCURO)
        ).strip().upper()

        if resposta != "S":
            print()
            print("Operação cancelada.")
            input("\nPressione ENTER para continuar...")
            return

        self.repository.excluir(id_usuario)
        print()
        input("Pressione ENTER para continuar...")
