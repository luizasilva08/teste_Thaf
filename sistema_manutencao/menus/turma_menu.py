from models.turma import Turma
from repositories.turma_repository import TurmaRepository
from utils.turma_validacoes import validar_codigo_turma, validar_periodo_turma

from menus.gradiente import gradiente_texto


class MenuTurma:

    # Verde oficina: verde escuro -> verde -> verde claro
    VERDE_ESCURO = (10, 40, 20)
    VERDE = (40, 140, 70)
    VERDE_CLARO = (170, 230, 190)

    def __init__(self):
        self.repository = TurmaRepository()

    # submenu
    def exibir(self):
        while True:
            print()
            print(gradiente_texto("=" * 60, self.VERDE_ESCURO, self.VERDE_CLARO))
            print(gradiente_texto("CTW MANUTENÇÃO - TURMAS", self.VERDE, self.VERDE_CLARO))
            print(gradiente_texto("=" * 60, self.VERDE_CLARO, self.VERDE_ESCURO))
            print(gradiente_texto("1 - Cadastrar Turma", self.VERDE_ESCURO, self.VERDE))
            print(gradiente_texto("2 - Buscar Turma", self.VERDE_ESCURO, self.VERDE))
            print(gradiente_texto("3 - Listar Turmas", self.VERDE, self.VERDE_CLARO))
            print(gradiente_texto("4 - Atualizar Turma", self.VERDE, self.VERDE_CLARO))
            print(gradiente_texto("5 - Excluir Turma", self.VERDE_ESCURO, self.VERDE_CLARO))
            print(gradiente_texto("0 - Sair", self.VERDE_ESCURO, self.VERDE))
            print(gradiente_texto("=" * 60, self.VERDE_CLARO, self.VERDE_ESCURO))

            opcao = input(gradiente_texto("Escolha uma opção: ", self.VERDE_CLARO, self.VERDE_ESCURO))

            if opcao == "1":
                self.cadastrar_turma()

            elif opcao == "2":
                self.buscar_turma()

            elif opcao == "3":
                self.listar_turma()

            elif opcao == "4":
                self.atualizar_turma()

            elif opcao == "5":
                self.excluir_turma()

            elif opcao == "0":
                self.repository.fechar()
                print()
                print(gradiente_texto("Voltando ao menu principal...", self.VERDE_ESCURO, self.VERDE))
                break

            else:
                print()
                print(gradiente_texto("Opção inválida!", self.VERDE_CLARO, self.VERDE_ESCURO))

    def cadastrar_turma(self):
        print()
        print(gradiente_texto("=" * 60, self.VERDE_ESCURO, self.VERDE_CLARO))
        print(gradiente_texto("CADASTRO DE TURMA", self.VERDE, self.VERDE_CLARO))
        print(gradiente_texto("=" * 60, self.VERDE_CLARO, self.VERDE_ESCURO))

        try:
            codigo_turma = validar_codigo_turma(
                input(gradiente_texto("Código (ex: MAN-2026-2T): ", self.VERDE_ESCURO, self.VERDE))
            )
            periodo_turma = validar_periodo_turma(
                input(gradiente_texto("Período (ex: Primeiro Turno): ", self.VERDE, self.VERDE_CLARO))
            )

        except ValueError as erro:
            print()
            print(gradiente_texto(f"Erro: {erro}", self.VERDE_CLARO, self.VERDE_ESCURO))
            input("\nPressione ENTER para continuar...")
            return

        turma = Turma(
            codigo_turma=codigo_turma,
            periodo_turma=periodo_turma
        )
        self.repository.salvar(turma)
        print()
        input("Pressione ENTER para continuar...")

    def buscar_turma(self):
        print()
        print(gradiente_texto("=" * 60, self.VERDE_ESCURO, self.VERDE_CLARO))
        print(gradiente_texto("BUSCAR TURMA", self.VERDE, self.VERDE_CLARO))
        print(gradiente_texto("=" * 60, self.VERDE_CLARO, self.VERDE_ESCURO))

        try:
            id_turma = int(
                input(gradiente_texto("Código (id) da turma: ", self.VERDE_ESCURO, self.VERDE))
            )

        except ValueError:
            print()
            print("Código inválido.")
            input("\nPressione ENTER para continuar...")
            return

        turma = self.repository.buscar_por_id(id_turma)
        print()

        if turma is None:
            print("Turma não encontrada.")

        else:
            print(gradiente_texto(f"Código......: {turma.id_turma}", self.VERDE_ESCURO, self.VERDE))
            print(gradiente_texto(f"Sigla.......: {turma.codigo_turma}", self.VERDE, self.VERDE_CLARO))
            print(gradiente_texto(f"Período.....: {turma.periodo_turma}", self.VERDE_CLARO, self.VERDE_ESCURO))

        print()
        input("Pressione ENTER para continuar...")

    def listar_turma(self):
        print()
        print(gradiente_texto("=" * 60, self.VERDE_ESCURO, self.VERDE_CLARO))
        print(gradiente_texto("LISTA DE TURMAS", self.VERDE, self.VERDE_CLARO))
        print(gradiente_texto("=" * 60, self.VERDE_CLARO, self.VERDE_ESCURO))
        turmas = self.repository.listar()

        if not turmas:
            print()
            print("Nenhuma turma cadastrada.")
            print()
            input("Pressione ENTER para continuar...")
            return

        print(
            gradiente_texto(
                f"{'ID':<5}{'Código':<20}{'Período':<25}",
                self.VERDE_ESCURO, self.VERDE_CLARO
            )
        )
        print(gradiente_texto("-" * 60, self.VERDE_CLARO, self.VERDE_ESCURO))

        for turma in turmas:
            print(
                gradiente_texto(
                    f"{turma.id_turma:<5}{turma.codigo_turma:<20}{turma.periodo_turma:<25}",
                    self.VERDE, self.VERDE_CLARO
                )
            )

        print()
        print(gradiente_texto(f"Total de turmas: {len(turmas)}", self.VERDE, self.VERDE_CLARO))
        print()
        input("Pressione ENTER para continuar...")

    def atualizar_turma(self):
        print()
        print(gradiente_texto("=" * 60, self.VERDE_ESCURO, self.VERDE_CLARO))
        print(gradiente_texto("ATUALIZAÇÃO DE TURMA", self.VERDE, self.VERDE_CLARO))
        print(gradiente_texto("=" * 60, self.VERDE_CLARO, self.VERDE_ESCURO))

        try:
            id_turma = int(
                input(gradiente_texto("Código (id) da turma: ", self.VERDE_ESCURO, self.VERDE))
            )

        except ValueError:
            print()
            print("Código inválido.")
            input("\nPressione ENTER para continuar...")
            return

        turma = self.repository.buscar_por_id(id_turma)

        if turma is None:
            print()
            print("Turma não encontrada.")
            input("\nPressione ENTER para continuar...")
            return

        print()
        print(gradiente_texto("Pressione ENTER para manter o valor atual.", self.VERDE, self.VERDE_CLARO))
        print()

        codigo_turma = input(
            gradiente_texto(f"Código [{turma.codigo_turma}]: ", self.VERDE_ESCURO, self.VERDE)
        )
        if codigo_turma:
            try:
                turma.codigo_turma = validar_codigo_turma(codigo_turma)
            except ValueError as erro:
                print(gradiente_texto(f"Erro: {erro}", self.VERDE_CLARO, self.VERDE_ESCURO))
                input("\nPressione ENTER para continuar...")
                return

        periodo_turma = input(
            gradiente_texto(f"Período [{turma.periodo_turma}]: ", self.VERDE, self.VERDE_CLARO)
        )
        if periodo_turma:
            turma.periodo_turma = periodo_turma

        self.repository.atualizar(turma)
        print()
        input("Pressione ENTER para continuar...")

    def excluir_turma(self):
        print()
        print(gradiente_texto("=" * 60, self.VERDE_ESCURO, self.VERDE_CLARO))
        print(gradiente_texto("EXCLUSÃO DE TURMA", self.VERDE, self.VERDE_CLARO))
        print(gradiente_texto("=" * 60, self.VERDE_CLARO, self.VERDE_ESCURO))

        try:
            id_turma = int(
                input(gradiente_texto("Código (id) da turma: ", self.VERDE_ESCURO, self.VERDE))
            )

        except ValueError:
            print()
            print("Código inválido.")
            input("\nPressione ENTER para continuar...")
            return

        turma = self.repository.buscar_por_id(id_turma)

        if turma is None:
            print()
            print("Turma não encontrada.")
            input("\nPressione ENTER para continuar...")
            return

        print()
        print(gradiente_texto("Turma localizada", self.VERDE, self.VERDE_CLARO))
        print(gradiente_texto("-" * 60, self.VERDE_CLARO, self.VERDE_ESCURO))
        print(gradiente_texto(f"Código.....: {turma.id_turma}", self.VERDE_ESCURO, self.VERDE))
        print(gradiente_texto(f"Sigla......: {turma.codigo_turma}", self.VERDE, self.VERDE_CLARO))
        print()

        resposta = input(
            gradiente_texto("Deseja realmente excluir esta turma? (S/N): ", self.VERDE_CLARO, self.VERDE_ESCURO)
        ).strip().upper()

        if resposta != "S":
            print()
            print("Operação cancelada.")
            input("\nPressione ENTER para continuar...")
            return

        self.repository.excluir(id_turma)
        print()
        input("Pressione ENTER para continuar...")
