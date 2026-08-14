from models.perfil import Perfil
from repositories.perfil_repository import PerfilRepository
from soft_delete.perfil_soft_delete import PerfilSoftDelete
from utils.perfil_validacoes import validar_nome_perfil

from menus.gradiente import gradiente_texto


class MenuPerfil:

    # Laranja segurança: aço escuro -> laranja industrial -> âmbar claro
    ACO_ESCURO = (30, 34, 40)
    LARANJA = (217, 98, 43)
    AMBAR = (240, 180, 110)

    def __init__(self):
        self.repository = PerfilRepository()
        self.soft_delete = PerfilSoftDelete()

    # submenu
    def exibir(self):
        while True:
            print()
            print(gradiente_texto("=" * 60, self.ACO_ESCURO, self.AMBAR))
            print(gradiente_texto("CTW MANUTENÇÃO - PERFIS DE ACESSO", self.LARANJA, self.AMBAR))
            print(gradiente_texto("=" * 60, self.AMBAR, self.ACO_ESCURO))
            print(gradiente_texto("1 - Cadastrar Perfil", self.ACO_ESCURO, self.LARANJA))
            print(gradiente_texto("2 - Buscar Perfil", self.ACO_ESCURO, self.LARANJA))
            print(gradiente_texto("3 - Listar Perfis", self.LARANJA, self.AMBAR))
            print(gradiente_texto("4 - Atualizar Perfil", self.LARANJA, self.AMBAR))
            print(gradiente_texto("5 - Excluir Perfil", self.ACO_ESCURO, self.AMBAR))
            print(gradiente_texto("6 - Ver Perfis Excluídos", self.ACO_ESCURO, self.AMBAR))
            print(gradiente_texto("7 - Restaurar Perfil Excluído", self.ACO_ESCURO, self.AMBAR))
            print(gradiente_texto("0 - Sair", self.ACO_ESCURO, self.LARANJA))
            print(gradiente_texto("=" * 60, self.AMBAR, self.ACO_ESCURO))

            opcao = input(gradiente_texto("Escolha uma opção: ", self.AMBAR, self.ACO_ESCURO))

            if opcao == "1":
                self.cadastrar_perfil()

            elif opcao == "2":
                self.buscar_perfil()

            elif opcao == "3":
                self.listar_perfil()

            elif opcao == "4":
                self.atualizar_perfil()

            elif opcao == "5":
                self.excluir_perfil()

            elif opcao == "6":
                self.listar_perfis_excluidos()

            elif opcao == "7":
                self.restaurar_perfil()

            elif opcao == "0":
                self.repository.fechar()
                self.soft_delete.fechar()
                print()
                print(gradiente_texto("Voltando ao menu principal...", self.ACO_ESCURO, self.LARANJA))
                break

            else:
                print()
                print(gradiente_texto("Opção inválida!", self.AMBAR, self.ACO_ESCURO))

    def cadastrar_perfil(self):
        print()
        print(gradiente_texto("=" * 60, self.ACO_ESCURO, self.AMBAR))
        print(gradiente_texto("CADASTRO DE PERFIL", self.LARANJA, self.AMBAR))
        print(gradiente_texto("=" * 60, self.AMBAR, self.ACO_ESCURO))

        try:
            nome_perfil = validar_nome_perfil(
                input(gradiente_texto("Nome (coordenador/gestor/professor/aluno): ", self.ACO_ESCURO, self.LARANJA))
            )
            descricao_perfil = input(gradiente_texto("Descrição: ", self.LARANJA, self.AMBAR))

        except ValueError as erro:
            print()
            print(gradiente_texto(f"Erro: {erro}", self.AMBAR, self.ACO_ESCURO))
            input("\nPressione ENTER para continuar...")
            return

        perfil = Perfil(
            nome_perfil=nome_perfil,
            descricao_perfil=descricao_perfil
        )
        self.repository.salvar(perfil)
        print()
        input("Pressione ENTER para continuar...")

    def buscar_perfil(self):
        print()
        print(gradiente_texto("=" * 60, self.ACO_ESCURO, self.AMBAR))
        print(gradiente_texto("BUSCAR PERFIL", self.LARANJA, self.AMBAR))
        print(gradiente_texto("=" * 60, self.AMBAR, self.ACO_ESCURO))

        try:
            id_perfil = int(
                input(gradiente_texto("Código do perfil: ", self.ACO_ESCURO, self.LARANJA))
            )

        except ValueError:
            print()
            print("Código inválido.")
            input("\nPressione ENTER para continuar...")
            return

        perfil = self.repository.buscar_por_id(id_perfil)
        print()

        if perfil is None:
            print("Perfil não encontrado.")

        else:
            print(gradiente_texto(f"Código......: {perfil.id_perfil}", self.ACO_ESCURO, self.LARANJA))
            print(gradiente_texto(f"Nome........: {perfil.nome_perfil}", self.LARANJA, self.AMBAR))
            print(gradiente_texto(f"Descrição...: {perfil.descricao_perfil}", self.AMBAR, self.ACO_ESCURO))

        print()
        input("Pressione ENTER para continuar...")

    def listar_perfil(self):
        print()
        print(gradiente_texto("=" * 60, self.ACO_ESCURO, self.AMBAR))
        print(gradiente_texto("LISTA DE PERFIS", self.LARANJA, self.AMBAR))
        print(gradiente_texto("=" * 60, self.AMBAR, self.ACO_ESCURO))
        perfis = self.repository.listar()

        if not perfis:
            print()
            print("Nenhum perfil cadastrado.")
            print()
            input("Pressione ENTER para continuar...")
            return

        print(
            gradiente_texto(
                f"{'ID':<5}{'Nome':<20}{'Descrição':<35}",
                self.ACO_ESCURO, self.AMBAR
            )
        )
        print(gradiente_texto("-" * 60, self.AMBAR, self.ACO_ESCURO))

        for perfil in perfis:
            print(
                gradiente_texto(
                    f"{perfil.id_perfil:<5}{perfil.nome_perfil:<20}{(perfil.descricao_perfil or ''):<35}",
                    self.LARANJA, self.AMBAR
                )
            )

        print()
        print(gradiente_texto(f"Total de perfis: {len(perfis)}", self.LARANJA, self.AMBAR))
        print()
        input("Pressione ENTER para continuar...")

    def atualizar_perfil(self):
        print()
        print(gradiente_texto("=" * 60, self.ACO_ESCURO, self.AMBAR))
        print(gradiente_texto("ATUALIZAÇÃO DE PERFIL", self.LARANJA, self.AMBAR))
        print(gradiente_texto("=" * 60, self.AMBAR, self.ACO_ESCURO))

        try:
            id_perfil = int(
                input(gradiente_texto("Código do perfil: ", self.ACO_ESCURO, self.LARANJA))
            )

        except ValueError:
            print()
            print("Código inválido.")
            input("\nPressione ENTER para continuar...")
            return

        perfil = self.repository.buscar_por_id(id_perfil)

        if perfil is None:
            print()
            print("Perfil não encontrado.")
            input("\nPressione ENTER para continuar...")
            return

        print()
        print(gradiente_texto("Pressione ENTER para manter o valor atual.", self.LARANJA, self.AMBAR))
        print()

        nome_perfil = input(
            gradiente_texto(f"Nome [{perfil.nome_perfil}]: ", self.ACO_ESCURO, self.LARANJA)
        )
        if nome_perfil:
            try:
                perfil.nome_perfil = validar_nome_perfil(nome_perfil)
            except ValueError as erro:
                print(gradiente_texto(f"Erro: {erro}", self.AMBAR, self.ACO_ESCURO))
                input("\nPressione ENTER para continuar...")
                return

        descricao_perfil = input(
            gradiente_texto(f"Descrição [{perfil.descricao_perfil}]: ", self.LARANJA, self.AMBAR)
        )
        if descricao_perfil:
            perfil.descricao_perfil = descricao_perfil

        self.repository.atualizar(perfil)
        print()
        input("Pressione ENTER para continuar...")

    def excluir_perfil(self):
        print()
        print(gradiente_texto("=" * 60, self.ACO_ESCURO, self.AMBAR))
        print(gradiente_texto("EXCLUSÃO DE PERFIL", self.LARANJA, self.AMBAR))
        print(gradiente_texto("=" * 60, self.AMBAR, self.ACO_ESCURO))

        try:
            id_perfil = int(
                input(gradiente_texto("Código do perfil: ", self.ACO_ESCURO, self.LARANJA))
            )

        except ValueError:
            print()
            print("Código inválido.")
            input("\nPressione ENTER para continuar...")
            return

        perfil = self.repository.buscar_por_id(id_perfil)

        if perfil is None:
            print()
            print("Perfil não encontrado.")
            input("\nPressione ENTER para continuar...")
            return

        print()
        print(gradiente_texto("Perfil localizado", self.LARANJA, self.AMBAR))
        print(gradiente_texto("-" * 60, self.AMBAR, self.ACO_ESCURO))
        print(gradiente_texto(f"Código.....: {perfil.id_perfil}", self.ACO_ESCURO, self.LARANJA))
        print(gradiente_texto(f"Nome.......: {perfil.nome_perfil}", self.LARANJA, self.AMBAR))
        print()

        resposta = input(
            gradiente_texto("Deseja realmente excluir este perfil? (S/N): ", self.AMBAR, self.ACO_ESCURO)
        ).strip().upper()

        if resposta != "S":
            print()
            print("Operação cancelada.")
            input("\nPressione ENTER para continuar...")
            return

        self.repository.excluir(id_perfil)
        print()
        input("Pressione ENTER para continuar...")

    def listar_perfis_excluidos(self):
        print()
        print(gradiente_texto("=" * 60, self.ACO_ESCURO, self.AMBAR))
        print(gradiente_texto("PERFIS EXCLUÍDOS", self.LARANJA, self.AMBAR))
        print(gradiente_texto("=" * 60, self.AMBAR, self.ACO_ESCURO))
        perfis = self.soft_delete.listar_excluidos()

        if not perfis:
            print()
            print("Nenhum perfil excluído.")
            print()
            input("Pressione ENTER para continuar...")
            return

        print(
            gradiente_texto(
                f"{'ID':<5}{'Nome':<20}{'Excluído em':<25}",
                self.ACO_ESCURO, self.AMBAR
            )
        )
        print(gradiente_texto("-" * 60, self.AMBAR, self.ACO_ESCURO))

        for perfil in perfis:
            print(
                gradiente_texto(
                    f"{perfil.id_perfil:<5}{perfil.nome_perfil:<20}{str(perfil.deleted_at):<25}",
                    self.LARANJA, self.AMBAR
                )
            )

        print()
        print(gradiente_texto(f"Total de perfis excluídos: {len(perfis)}", self.LARANJA, self.AMBAR))
        print()
        input("Pressione ENTER para continuar...")

    def restaurar_perfil(self):
        print()
        print(gradiente_texto("=" * 60, self.ACO_ESCURO, self.AMBAR))
        print(gradiente_texto("RESTAURAR PERFIL EXCLUÍDO", self.LARANJA, self.AMBAR))
        print(gradiente_texto("=" * 60, self.AMBAR, self.ACO_ESCURO))

        try:
            id_perfil = int(
                input(gradiente_texto("Código do perfil excluído: ", self.ACO_ESCURO, self.LARANJA))
            )

        except ValueError:
            print()
            print("Código inválido.")
            input("\nPressione ENTER para continuar...")
            return

        perfil = self.soft_delete.buscar_excluido_por_id(id_perfil)

        if perfil is None:
            print()
            print("Perfil excluído não encontrado.")
            input("\nPressione ENTER para continuar...")
            return

        print()
        print(gradiente_texto(f"Perfil localizado: {perfil.nome_perfil}", self.LARANJA, self.AMBAR))

        resposta = input(
            gradiente_texto("Deseja restaurar este perfil? (S/N): ", self.AMBAR, self.ACO_ESCURO)
        ).strip().upper()

        if resposta != "S":
            print()
            print("Operação cancelada.")
            input("\nPressione ENTER para continuar...")
            return

        self.soft_delete.restaurar(id_perfil)
        print()
        input("Pressione ENTER para continuar...")
