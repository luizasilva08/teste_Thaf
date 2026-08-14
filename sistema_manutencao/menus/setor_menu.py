from models.setor import Setor
from repositories.setor_repository import SetorRepository
from utils.setor_validacoes import validar_nome_setor

from menus.gradiente import gradiente_texto


class MenuSetor:

    # Amarelo industrial: âmbar escuro -> amarelo -> amarelo claro
    AMBAR_ESCURO = (60, 45, 5)
    AMARELO = (200, 150, 20)
    AMARELO_CLARO = (240, 220, 150)

    def __init__(self):
        self.repository = SetorRepository()

    # submenu
    def exibir(self):
        while True:
            print()
            print(gradiente_texto("=" * 60, self.AMBAR_ESCURO, self.AMARELO_CLARO))
            print(gradiente_texto("CTW MANUTENÇÃO - SETORES", self.AMARELO, self.AMARELO_CLARO))
            print(gradiente_texto("=" * 60, self.AMARELO_CLARO, self.AMBAR_ESCURO))
            print(gradiente_texto("1 - Cadastrar Setor", self.AMBAR_ESCURO, self.AMARELO))
            print(gradiente_texto("2 - Buscar Setor", self.AMBAR_ESCURO, self.AMARELO))
            print(gradiente_texto("3 - Listar Setores", self.AMARELO, self.AMARELO_CLARO))
            print(gradiente_texto("4 - Atualizar Setor", self.AMARELO, self.AMARELO_CLARO))
            print(gradiente_texto("5 - Excluir Setor", self.AMBAR_ESCURO, self.AMARELO_CLARO))
            print(gradiente_texto("0 - Sair", self.AMBAR_ESCURO, self.AMARELO))
            print(gradiente_texto("=" * 60, self.AMARELO_CLARO, self.AMBAR_ESCURO))

            opcao = input(gradiente_texto("Escolha uma opção: ", self.AMARELO_CLARO, self.AMBAR_ESCURO))

            if opcao == "1":
                self.cadastrar_setor()

            elif opcao == "2":
                self.buscar_setor()

            elif opcao == "3":
                self.listar_setor()

            elif opcao == "4":
                self.atualizar_setor()

            elif opcao == "5":
                self.excluir_setor()

            elif opcao == "0":
                self.repository.fechar()
                print()
                print(gradiente_texto("Voltando ao menu principal...", self.AMBAR_ESCURO, self.AMARELO))
                break

            else:
                print()
                print(gradiente_texto("Opção inválida!", self.AMARELO_CLARO, self.AMBAR_ESCURO))

    def cadastrar_setor(self):
        print()
        print(gradiente_texto("=" * 60, self.AMBAR_ESCURO, self.AMARELO_CLARO))
        print(gradiente_texto("CADASTRO DE SETOR", self.AMARELO, self.AMARELO_CLARO))
        print(gradiente_texto("=" * 60, self.AMARELO_CLARO, self.AMBAR_ESCURO))

        try:
            nome = validar_nome_setor(
                input(gradiente_texto("Nome do setor (ex: Usinagem): ", self.AMBAR_ESCURO, self.AMARELO))
            )
            descricao = input(gradiente_texto("Descrição: ", self.AMARELO, self.AMARELO_CLARO))

        except ValueError as erro:
            print()
            print(gradiente_texto(f"Erro: {erro}", self.AMARELO_CLARO, self.AMBAR_ESCURO))
            input("\nPressione ENTER para continuar...")
            return

        setor = Setor(
            nome=nome,
            descricao=descricao
        )
        self.repository.salvar(setor)
        print()
        input("Pressione ENTER para continuar...")

    def buscar_setor(self):
        print()
        print(gradiente_texto("=" * 60, self.AMBAR_ESCURO, self.AMARELO_CLARO))
        print(gradiente_texto("BUSCAR SETOR", self.AMARELO, self.AMARELO_CLARO))
        print(gradiente_texto("=" * 60, self.AMARELO_CLARO, self.AMBAR_ESCURO))

        try:
            id_setor = int(
                input(gradiente_texto("Código do setor: ", self.AMBAR_ESCURO, self.AMARELO))
            )

        except ValueError:
            print()
            print("Código inválido.")
            input("\nPressione ENTER para continuar...")
            return

        setor = self.repository.buscar_por_id(id_setor)
        print()

        if setor is None:
            print("Setor não encontrado.")

        else:
            print(gradiente_texto(f"Código......: {setor.id_setor}", self.AMBAR_ESCURO, self.AMARELO))
            print(gradiente_texto(f"Nome........: {setor.nome}", self.AMARELO, self.AMARELO_CLARO))
            print(gradiente_texto(f"Descrição...: {setor.descricao}", self.AMARELO_CLARO, self.AMBAR_ESCURO))

        print()
        input("Pressione ENTER para continuar...")

    def listar_setor(self):
        print()
        print(gradiente_texto("=" * 60, self.AMBAR_ESCURO, self.AMARELO_CLARO))
        print(gradiente_texto("LISTA DE SETORES", self.AMARELO, self.AMARELO_CLARO))
        print(gradiente_texto("=" * 60, self.AMARELO_CLARO, self.AMBAR_ESCURO))
        setores = self.repository.listar()

        if not setores:
            print()
            print("Nenhum setor cadastrado.")
            print()
            input("Pressione ENTER para continuar...")
            return

        print(
            gradiente_texto(
                f"{'ID':<5}{'Nome':<20}{'Descrição':<35}",
                self.AMBAR_ESCURO, self.AMARELO_CLARO
            )
        )
        print(gradiente_texto("-" * 60, self.AMARELO_CLARO, self.AMBAR_ESCURO))

        for setor in setores:
            print(
                gradiente_texto(
                    f"{setor.id_setor:<5}{setor.nome:<20}{(setor.descricao or ''):<35}",
                    self.AMARELO, self.AMARELO_CLARO
                )
            )

        print()
        print(gradiente_texto(f"Total de setores: {len(setores)}", self.AMARELO, self.AMARELO_CLARO))
        print()
        input("Pressione ENTER para continuar...")

    def atualizar_setor(self):
        print()
        print(gradiente_texto("=" * 60, self.AMBAR_ESCURO, self.AMARELO_CLARO))
        print(gradiente_texto("ATUALIZAÇÃO DE SETOR", self.AMARELO, self.AMARELO_CLARO))
        print(gradiente_texto("=" * 60, self.AMARELO_CLARO, self.AMBAR_ESCURO))

        try:
            id_setor = int(
                input(gradiente_texto("Código do setor: ", self.AMBAR_ESCURO, self.AMARELO))
            )

        except ValueError:
            print()
            print("Código inválido.")
            input("\nPressione ENTER para continuar...")
            return

        setor = self.repository.buscar_por_id(id_setor)

        if setor is None:
            print()
            print("Setor não encontrado.")
            input("\nPressione ENTER para continuar...")
            return

        print()
        print(gradiente_texto("Pressione ENTER para manter o valor atual.", self.AMARELO, self.AMARELO_CLARO))
        print()

        nome = input(
            gradiente_texto(f"Nome [{setor.nome}]: ", self.AMBAR_ESCURO, self.AMARELO)
        )
        if nome:
            try:
                setor.nome = validar_nome_setor(nome)
            except ValueError as erro:
                print(gradiente_texto(f"Erro: {erro}", self.AMARELO_CLARO, self.AMBAR_ESCURO))
                input("\nPressione ENTER para continuar...")
                return

        descricao = input(
            gradiente_texto(f"Descrição [{setor.descricao}]: ", self.AMARELO, self.AMARELO_CLARO)
        )
        if descricao:
            setor.descricao = descricao

        self.repository.atualizar(setor)
        print()
        input("Pressione ENTER para continuar...")

    def excluir_setor(self):
        print()
        print(gradiente_texto("=" * 60, self.AMBAR_ESCURO, self.AMARELO_CLARO))
        print(gradiente_texto("EXCLUSÃO DE SETOR", self.AMARELO, self.AMARELO_CLARO))
        print(gradiente_texto("=" * 60, self.AMARELO_CLARO, self.AMBAR_ESCURO))

        try:
            id_setor = int(
                input(gradiente_texto("Código do setor: ", self.AMBAR_ESCURO, self.AMARELO))
            )

        except ValueError:
            print()
            print("Código inválido.")
            input("\nPressione ENTER para continuar...")
            return

        setor = self.repository.buscar_por_id(id_setor)

        if setor is None:
            print()
            print("Setor não encontrado.")
            input("\nPressione ENTER para continuar...")
            return

        print()
        print(gradiente_texto("Setor localizado", self.AMARELO, self.AMARELO_CLARO))
        print(gradiente_texto("-" * 60, self.AMARELO_CLARO, self.AMBAR_ESCURO))
        print(gradiente_texto(f"Código.....: {setor.id_setor}", self.AMBAR_ESCURO, self.AMARELO))
        print(gradiente_texto(f"Nome.......: {setor.nome}", self.AMARELO, self.AMARELO_CLARO))
        print()

        resposta = input(
            gradiente_texto("Deseja realmente excluir este setor? (S/N): ", self.AMARELO_CLARO, self.AMBAR_ESCURO)
        ).strip().upper()

        if resposta != "S":
            print()
            print("Operação cancelada.")
            input("\nPressione ENTER para continuar...")
            return

        self.repository.excluir(id_setor)
        print()
        input("Pressione ENTER para continuar...")
