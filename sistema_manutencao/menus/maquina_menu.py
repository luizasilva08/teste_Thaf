from models.maquina import STATUS_VALIDOS, Maquina
from repositories.maquina_repository import MaquinaRepository
from utils.maquina_validacoes import (
    validar_nome_maquina,
    validar_status_maquina,
    validar_tag_maquina,
)

from menus.gradiente import gradiente_texto


class MenuMaquina:

    # Ciano industrial: teal escuro -> teal -> teal claro
    TEAL_ESCURO = (5, 45, 50)
    TEAL = (20, 140, 150)
    TEAL_CLARO = (160, 225, 230)

    def __init__(self):
        self.repository = MaquinaRepository()

    # submenu
    def exibir(self):
        while True:
            print()
            print(gradiente_texto("=" * 60, self.TEAL_ESCURO, self.TEAL_CLARO))
            print(gradiente_texto("CTW MANUTENÇÃO - MÁQUINAS", self.TEAL, self.TEAL_CLARO))
            print(gradiente_texto("=" * 60, self.TEAL_CLARO, self.TEAL_ESCURO))
            print(gradiente_texto("1 - Cadastrar Máquina", self.TEAL_ESCURO, self.TEAL))
            print(gradiente_texto("2 - Buscar Máquina", self.TEAL_ESCURO, self.TEAL))
            print(gradiente_texto("3 - Listar Máquinas", self.TEAL, self.TEAL_CLARO))
            print(gradiente_texto("4 - Listar Máquinas por Setor", self.TEAL, self.TEAL_CLARO))
            print(gradiente_texto("5 - Listar Máquinas por Status", self.TEAL, self.TEAL_CLARO))
            print(gradiente_texto("6 - Atualizar Máquina", self.TEAL, self.TEAL_CLARO))
            print(gradiente_texto("7 - Atualizar Status", self.TEAL_ESCURO, self.TEAL_CLARO))
            print(gradiente_texto("8 - Registrar Manutenção Concluída", self.TEAL_ESCURO, self.TEAL_CLARO))
            print(gradiente_texto("9 - Excluir Máquina", self.TEAL_ESCURO, self.TEAL_CLARO))
            print(gradiente_texto("0 - Sair", self.TEAL_ESCURO, self.TEAL))
            print(gradiente_texto("=" * 60, self.TEAL_CLARO, self.TEAL_ESCURO))

            opcao = input(gradiente_texto("Escolha uma opção: ", self.TEAL_CLARO, self.TEAL_ESCURO))

            if opcao == "1":
                self.cadastrar_maquina()

            elif opcao == "2":
                self.buscar_maquina()

            elif opcao == "3":
                self.listar_maquina()

            elif opcao == "4":
                self.listar_maquina_por_setor()

            elif opcao == "5":
                self.listar_maquina_por_status()

            elif opcao == "6":
                self.atualizar_maquina()

            elif opcao == "7":
                self.atualizar_status()

            elif opcao == "8":
                self.registrar_manutencao_concluida()

            elif opcao == "9":
                self.excluir_maquina()

            elif opcao == "0":
                self.repository.fechar()
                print()
                print(gradiente_texto("Voltando ao menu principal...", self.TEAL_ESCURO, self.TEAL))
                break

            else:
                print()
                print(gradiente_texto("Opção inválida!", self.TEAL_CLARO, self.TEAL_ESCURO))

    def cadastrar_maquina(self):
        print()
        print(gradiente_texto("=" * 60, self.TEAL_ESCURO, self.TEAL_CLARO))
        print(gradiente_texto("CADASTRO DE MÁQUINA", self.TEAL, self.TEAL_CLARO))
        print(gradiente_texto("=" * 60, self.TEAL_CLARO, self.TEAL_ESCURO))

        try:
            setor_id = int(
                input(gradiente_texto("Código (id) do setor: ", self.TEAL_ESCURO, self.TEAL))
            )
            tag_maquina = validar_tag_maquina(
                input(gradiente_texto("Tag (ex: TOR-01): ", self.TEAL_ESCURO, self.TEAL))
            )
            nome_maquina = validar_nome_maquina(
                input(gradiente_texto("Nome da máquina: ", self.TEAL, self.TEAL_CLARO))
            )

        except ValueError as erro:
            print()
            print(gradiente_texto(f"Erro: {erro}", self.TEAL_CLARO, self.TEAL_ESCURO))
            input("\nPressione ENTER para continuar...")
            return

        maquina = Maquina(
            setor_id=setor_id,
            tag_maquina=tag_maquina,
            nome_maquina=nome_maquina
        )
        self.repository.salvar(maquina)
        print()
        input("Pressione ENTER para continuar...")

    def buscar_maquina(self):
        print()
        print(gradiente_texto("=" * 60, self.TEAL_ESCURO, self.TEAL_CLARO))
        print(gradiente_texto("BUSCAR MÁQUINA", self.TEAL, self.TEAL_CLARO))
        print(gradiente_texto("=" * 60, self.TEAL_CLARO, self.TEAL_ESCURO))

        try:
            id_maquina = int(
                input(gradiente_texto("Código da máquina: ", self.TEAL_ESCURO, self.TEAL))
            )

        except ValueError:
            print()
            print("Código inválido.")
            input("\nPressione ENTER para continuar...")
            return

        maquina = self.repository.buscar_por_id(id_maquina)
        print()

        if maquina is None:
            print("Máquina não encontrada.")

        else:
            print(gradiente_texto(f"Código..............: {maquina.id_maquina}", self.TEAL_ESCURO, self.TEAL))
            print(gradiente_texto(f"Tag.................: {maquina.tag_maquina}", self.TEAL, self.TEAL_CLARO))
            print(gradiente_texto(f"Nome................: {maquina.nome_maquina}", self.TEAL_CLARO, self.TEAL_ESCURO))
            print(gradiente_texto(f"Setor (id)..........: {maquina.setor_id}", self.TEAL_ESCURO, self.TEAL))
            print(gradiente_texto(f"Status..............: {maquina.status_vivo}", self.TEAL, self.TEAL_CLARO))
            print(gradiente_texto(f"Última manutenção...: {maquina.ultima_manutencao}", self.TEAL_CLARO, self.TEAL_ESCURO))

        print()
        input("Pressione ENTER para continuar...")

    def listar_maquina(self):
        print()
        print(gradiente_texto("=" * 60, self.TEAL_ESCURO, self.TEAL_CLARO))
        print(gradiente_texto("LISTA DE MÁQUINAS", self.TEAL, self.TEAL_CLARO))
        print(gradiente_texto("=" * 60, self.TEAL_CLARO, self.TEAL_ESCURO))
        self._imprimir_lista(self.repository.listar())

    def listar_maquina_por_setor(self):
        print()
        print(gradiente_texto("=" * 60, self.TEAL_ESCURO, self.TEAL_CLARO))
        print(gradiente_texto("MÁQUINAS POR SETOR", self.TEAL, self.TEAL_CLARO))
        print(gradiente_texto("=" * 60, self.TEAL_CLARO, self.TEAL_ESCURO))

        try:
            setor_id = int(
                input(gradiente_texto("Código (id) do setor: ", self.TEAL_ESCURO, self.TEAL))
            )

        except ValueError:
            print()
            print("Código inválido.")
            input("\nPressione ENTER para continuar...")
            return

        self._imprimir_lista(self.repository.listar_por_setor(setor_id))

    def listar_maquina_por_status(self):
        print()
        print(gradiente_texto("=" * 60, self.TEAL_ESCURO, self.TEAL_CLARO))
        print(gradiente_texto("MÁQUINAS POR STATUS", self.TEAL, self.TEAL_CLARO))
        print(gradiente_texto("=" * 60, self.TEAL_CLARO, self.TEAL_ESCURO))

        try:
            status_vivo = validar_status_maquina(
                input(gradiente_texto(f"Status {STATUS_VALIDOS}: ", self.TEAL_ESCURO, self.TEAL))
            )

        except ValueError as erro:
            print()
            print(gradiente_texto(f"Erro: {erro}", self.TEAL_CLARO, self.TEAL_ESCURO))
            input("\nPressione ENTER para continuar...")
            return

        self._imprimir_lista(self.repository.listar_por_status(status_vivo))

    def _imprimir_lista(self, maquinas):
        if not maquinas:
            print()
            print("Nenhuma máquina encontrada.")
            print()
            input("Pressione ENTER para continuar...")
            return

        print(
            gradiente_texto(
                f"{'ID':<5}{'Tag':<12}{'Nome':<25}{'Setor':<8}{'Status':<12}",
                self.TEAL_ESCURO, self.TEAL_CLARO
            )
        )
        print(gradiente_texto("-" * 70, self.TEAL_CLARO, self.TEAL_ESCURO))

        for maquina in maquinas:
            print(
                gradiente_texto(
                    f"{maquina.id_maquina:<5}{maquina.tag_maquina:<12}{maquina.nome_maquina:<25}{maquina.setor_id:<8}{maquina.status_vivo:<12}",
                    self.TEAL, self.TEAL_CLARO
                )
            )

        print()
        print(gradiente_texto(f"Total de máquinas: {len(maquinas)}", self.TEAL, self.TEAL_CLARO))
        print()
        input("Pressione ENTER para continuar...")

    def atualizar_maquina(self):
        print()
        print(gradiente_texto("=" * 60, self.TEAL_ESCURO, self.TEAL_CLARO))
        print(gradiente_texto("ATUALIZAÇÃO DE MÁQUINA", self.TEAL, self.TEAL_CLARO))
        print(gradiente_texto("=" * 60, self.TEAL_CLARO, self.TEAL_ESCURO))

        try:
            id_maquina = int(
                input(gradiente_texto("Código da máquina: ", self.TEAL_ESCURO, self.TEAL))
            )

        except ValueError:
            print()
            print("Código inválido.")
            input("\nPressione ENTER para continuar...")
            return

        maquina = self.repository.buscar_por_id(id_maquina)

        if maquina is None:
            print()
            print("Máquina não encontrada.")
            input("\nPressione ENTER para continuar...")
            return

        print()
        print(gradiente_texto("Pressione ENTER para manter o valor atual.", self.TEAL, self.TEAL_CLARO))
        print()

        tag_maquina = input(
            gradiente_texto(f"Tag [{maquina.tag_maquina}]: ", self.TEAL_ESCURO, self.TEAL)
        )
        if tag_maquina:
            try:
                maquina.tag_maquina = validar_tag_maquina(tag_maquina)
            except ValueError as erro:
                print(gradiente_texto(f"Erro: {erro}", self.TEAL_CLARO, self.TEAL_ESCURO))
                input("\nPressione ENTER para continuar...")
                return

        nome_maquina = input(
            gradiente_texto(f"Nome [{maquina.nome_maquina}]: ", self.TEAL, self.TEAL_CLARO)
        )
        if nome_maquina:
            try:
                maquina.nome_maquina = validar_nome_maquina(nome_maquina)
            except ValueError as erro:
                print(gradiente_texto(f"Erro: {erro}", self.TEAL_CLARO, self.TEAL_ESCURO))
                input("\nPressione ENTER para continuar...")
                return

        setor_id = input(
            gradiente_texto(f"Código (id) do setor [{maquina.setor_id}]: ", self.TEAL_CLARO, self.TEAL_ESCURO)
        )
        if setor_id:
            maquina.setor_id = int(setor_id)

        self.repository.atualizar(maquina)
        print()
        input("Pressione ENTER para continuar...")

    def atualizar_status(self):
        print()
        print(gradiente_texto("=" * 60, self.TEAL_ESCURO, self.TEAL_CLARO))
        print(gradiente_texto("ATUALIZAR STATUS DA MÁQUINA", self.TEAL, self.TEAL_CLARO))
        print(gradiente_texto("=" * 60, self.TEAL_CLARO, self.TEAL_ESCURO))

        try:
            id_maquina = int(
                input(gradiente_texto("Código da máquina: ", self.TEAL_ESCURO, self.TEAL))
            )
            status_vivo = validar_status_maquina(
                input(gradiente_texto(f"Novo status {STATUS_VALIDOS}: ", self.TEAL, self.TEAL_CLARO))
            )

        except ValueError as erro:
            print()
            print(gradiente_texto(f"Erro: {erro}", self.TEAL_CLARO, self.TEAL_ESCURO))
            input("\nPressione ENTER para continuar...")
            return

        self.repository.atualizar_status(id_maquina, status_vivo)
        print()
        input("Pressione ENTER para continuar...")

    def registrar_manutencao_concluida(self):
        print()
        print(gradiente_texto("=" * 60, self.TEAL_ESCURO, self.TEAL_CLARO))
        print(gradiente_texto("REGISTRAR MANUTENÇÃO CONCLUÍDA", self.TEAL, self.TEAL_CLARO))
        print(gradiente_texto("=" * 60, self.TEAL_CLARO, self.TEAL_ESCURO))

        try:
            id_maquina = int(
                input(gradiente_texto("Código da máquina: ", self.TEAL_ESCURO, self.TEAL))
            )

        except ValueError:
            print()
            print("Código inválido.")
            input("\nPressione ENTER para continuar...")
            return

        self.repository.registrar_manutencao_concluida(id_maquina)
        print()
        input("Pressione ENTER para continuar...")

    def excluir_maquina(self):
        print()
        print(gradiente_texto("=" * 60, self.TEAL_ESCURO, self.TEAL_CLARO))
        print(gradiente_texto("EXCLUSÃO DE MÁQUINA", self.TEAL, self.TEAL_CLARO))
        print(gradiente_texto("=" * 60, self.TEAL_CLARO, self.TEAL_ESCURO))

        try:
            id_maquina = int(
                input(gradiente_texto("Código da máquina: ", self.TEAL_ESCURO, self.TEAL))
            )

        except ValueError:
            print()
            print("Código inválido.")
            input("\nPressione ENTER para continuar...")
            return

        maquina = self.repository.buscar_por_id(id_maquina)

        if maquina is None:
            print()
            print("Máquina não encontrada.")
            input("\nPressione ENTER para continuar...")
            return

        print()
        print(gradiente_texto("Máquina localizada", self.TEAL, self.TEAL_CLARO))
        print(gradiente_texto("-" * 60, self.TEAL_CLARO, self.TEAL_ESCURO))
        print(gradiente_texto(f"Código.....: {maquina.id_maquina}", self.TEAL_ESCURO, self.TEAL))
        print(gradiente_texto(f"Tag........: {maquina.tag_maquina}", self.TEAL, self.TEAL_CLARO))
        print()

        resposta = input(
            gradiente_texto("Deseja realmente excluir esta máquina? (S/N): ", self.TEAL_CLARO, self.TEAL_ESCURO)
        ).strip().upper()

        if resposta != "S":
            print()
            print("Operação cancelada.")
            input("\nPressione ENTER para continuar...")
            return

        self.repository.excluir(id_maquina)
        print()
        input("Pressione ENTER para continuar...")
