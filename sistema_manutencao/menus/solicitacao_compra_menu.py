from models.solicitacao_compra import STATUS_VALIDOS, SolicitacaoCompra
from repositories.solicitacao_compra_repository import SolicitacaoCompraRepository
from utils.solicitacao_compra_validacoes import (
    validar_especificacao_tecnica,
    validar_justificativa,
    validar_status_compra,
)

from menus.gradiente import gradiente_texto


class MenuSolicitacaoCompra:

    # Turquesa: verde-água escuro -> turquesa -> claro
    TURQUESA_ESCURO = (5, 40, 35)
    TURQUESA = (15, 150, 120)
    TURQUESA_CLARO = (150, 225, 205)

    def __init__(self):
        self.repository = SolicitacaoCompraRepository()

    # submenu
    def exibir(self):
        while True:
            print()
            print(gradiente_texto("=" * 60, self.TURQUESA_ESCURO, self.TURQUESA_CLARO))
            print(gradiente_texto("CTW MANUTENÇÃO - SOLICITAÇÕES DE COMPRA", self.TURQUESA, self.TURQUESA_CLARO))
            print(gradiente_texto("=" * 60, self.TURQUESA_CLARO, self.TURQUESA_ESCURO))
            print(gradiente_texto("1 - Abrir Solicitação", self.TURQUESA_ESCURO, self.TURQUESA))
            print(gradiente_texto("2 - Buscar Solicitação", self.TURQUESA_ESCURO, self.TURQUESA))
            print(gradiente_texto("3 - Listar Solicitações", self.TURQUESA, self.TURQUESA_CLARO))
            print(gradiente_texto("4 - Listar por Status", self.TURQUESA, self.TURQUESA_CLARO))
            print(gradiente_texto("5 - Listar por Turma", self.TURQUESA, self.TURQUESA_CLARO))
            print(gradiente_texto("6 - Atualizar Status", self.TURQUESA_ESCURO, self.TURQUESA_CLARO))
            print(gradiente_texto("7 - Excluir Solicitação", self.TURQUESA_ESCURO, self.TURQUESA_CLARO))
            print(gradiente_texto("0 - Sair", self.TURQUESA_ESCURO, self.TURQUESA))
            print(gradiente_texto("=" * 60, self.TURQUESA_CLARO, self.TURQUESA_ESCURO))

            opcao = input(gradiente_texto("Escolha uma opção: ", self.TURQUESA_CLARO, self.TURQUESA_ESCURO))

            if opcao == "1":
                self.abrir_solicitacao()

            elif opcao == "2":
                self.buscar_solicitacao()

            elif opcao == "3":
                self.listar_solicitacao()

            elif opcao == "4":
                self.listar_por_status()

            elif opcao == "5":
                self.listar_por_turma()

            elif opcao == "6":
                self.atualizar_status()

            elif opcao == "7":
                self.excluir_solicitacao()

            elif opcao == "0":
                self.repository.fechar()
                print()
                print(gradiente_texto("Voltando ao menu principal...", self.TURQUESA_ESCURO, self.TURQUESA))
                break

            else:
                print()
                print(gradiente_texto("Opção inválida!", self.TURQUESA_CLARO, self.TURQUESA_ESCURO))

    def abrir_solicitacao(self):
        print()
        print(gradiente_texto("=" * 60, self.TURQUESA_ESCURO, self.TURQUESA_CLARO))
        print(gradiente_texto("ABRIR SOLICITAÇÃO DE COMPRA", self.TURQUESA, self.TURQUESA_CLARO))
        print(gradiente_texto("=" * 60, self.TURQUESA_CLARO, self.TURQUESA_ESCURO))

        try:
            solicitante_id = int(
                input(gradiente_texto("Código (id) do solicitante: ", self.TURQUESA_ESCURO, self.TURQUESA))
            )
            professor_responsavel_id = int(
                input(gradiente_texto("Código (id) do professor responsável: ", self.TURQUESA_ESCURO, self.TURQUESA))
            )
            especificacao_tecnica = validar_especificacao_tecnica(
                input(gradiente_texto("Especificação técnica: ", self.TURQUESA, self.TURQUESA_CLARO))
            )
            justificativa_solicitacao = validar_justificativa(
                input(gradiente_texto("Justificativa: ", self.TURQUESA, self.TURQUESA_CLARO))
            )
            quantidade_solicitacao = int(input(gradiente_texto("Quantidade [1]: ", self.TURQUESA_CLARO, self.TURQUESA_ESCURO)) or 1)
            equipamento = input(gradiente_texto("Equipamento (opcional): ", self.TURQUESA_ESCURO, self.TURQUESA)) or None

        except ValueError as erro:
            print()
            print(gradiente_texto(f"Erro: {erro}", self.TURQUESA_CLARO, self.TURQUESA_ESCURO))
            input("\nPressione ENTER para continuar...")
            return

        solicitacao = SolicitacaoCompra(
            solicitante_id=solicitante_id,
            professor_responsavel_id=professor_responsavel_id,
            especificacao_tecnica=especificacao_tecnica,
            justificativa_solicitacao=justificativa_solicitacao,
            quantidade_solicitacao=quantidade_solicitacao,
            equipamento=equipamento
        )
        self.repository.salvar(solicitacao)
        print()
        input("Pressione ENTER para continuar...")

    def buscar_solicitacao(self):
        print()
        print(gradiente_texto("=" * 60, self.TURQUESA_ESCURO, self.TURQUESA_CLARO))
        print(gradiente_texto("BUSCAR SOLICITAÇÃO DE COMPRA", self.TURQUESA, self.TURQUESA_CLARO))
        print(gradiente_texto("=" * 60, self.TURQUESA_CLARO, self.TURQUESA_ESCURO))

        try:
            id_solicitacao = int(
                input(gradiente_texto("Código da solicitação: ", self.TURQUESA_ESCURO, self.TURQUESA))
            )

        except ValueError:
            print()
            print("Código inválido.")
            input("\nPressione ENTER para continuar...")
            return

        solicitacao = self.repository.buscar_por_id(id_solicitacao)
        print()

        if solicitacao is None:
            print("Solicitação não encontrada.")

        else:
            print(gradiente_texto(f"Código..........: {solicitacao.id_solicitacao}", self.TURQUESA_ESCURO, self.TURQUESA))
            print(gradiente_texto(f"Especificação...: {solicitacao.especificacao_tecnica}", self.TURQUESA, self.TURQUESA_CLARO))
            print(gradiente_texto(f"Justificativa...: {solicitacao.justificativa_solicitacao}", self.TURQUESA_CLARO, self.TURQUESA_ESCURO))
            print(gradiente_texto(f"Quantidade......: {solicitacao.quantidade_solicitacao}", self.TURQUESA_ESCURO, self.TURQUESA))
            print(gradiente_texto(f"Status..........: {solicitacao.status}", self.TURQUESA, self.TURQUESA_CLARO))

        print()
        input("Pressione ENTER para continuar...")

    def listar_solicitacao(self):
        print()
        print(gradiente_texto("=" * 60, self.TURQUESA_ESCURO, self.TURQUESA_CLARO))
        print(gradiente_texto("LISTA DE SOLICITAÇÕES DE COMPRA", self.TURQUESA, self.TURQUESA_CLARO))
        print(gradiente_texto("=" * 60, self.TURQUESA_CLARO, self.TURQUESA_ESCURO))
        self._imprimir_lista(self.repository.listar())

    def listar_por_status(self):
        print()
        print(gradiente_texto("=" * 60, self.TURQUESA_ESCURO, self.TURQUESA_CLARO))
        print(gradiente_texto("SOLICITAÇÕES POR STATUS", self.TURQUESA, self.TURQUESA_CLARO))
        print(gradiente_texto("=" * 60, self.TURQUESA_CLARO, self.TURQUESA_ESCURO))

        try:
            status = validar_status_compra(
                input(gradiente_texto(f"Status {STATUS_VALIDOS}: ", self.TURQUESA_ESCURO, self.TURQUESA))
            )

        except ValueError as erro:
            print()
            print(gradiente_texto(f"Erro: {erro}", self.TURQUESA_CLARO, self.TURQUESA_ESCURO))
            input("\nPressione ENTER para continuar...")
            return

        self._imprimir_lista(self.repository.listar_por_status(status))

    def listar_por_turma(self):
        print()
        print(gradiente_texto("=" * 60, self.TURQUESA_ESCURO, self.TURQUESA_CLARO))
        print(gradiente_texto("SOLICITAÇÕES POR TURMA", self.TURQUESA, self.TURQUESA_CLARO))
        print(gradiente_texto("=" * 60, self.TURQUESA_CLARO, self.TURQUESA_ESCURO))

        try:
            turma_id = int(
                input(gradiente_texto("Código (id) da turma: ", self.TURQUESA_ESCURO, self.TURQUESA))
            )

        except ValueError:
            print()
            print("Código inválido.")
            input("\nPressione ENTER para continuar...")
            return

        self._imprimir_lista(self.repository.listar_por_turma(turma_id))

    def _imprimir_lista(self, solicitacoes):
        if not solicitacoes:
            print()
            print("Nenhuma solicitação encontrada.")
            print()
            input("Pressione ENTER para continuar...")
            return

        print(
            gradiente_texto(
                f"{'ID':<5}{'Especificação':<35}{'Qtd':<6}{'Status':<20}",
                self.TURQUESA_ESCURO, self.TURQUESA_CLARO
            )
        )
        print(gradiente_texto("-" * 66, self.TURQUESA_CLARO, self.TURQUESA_ESCURO))

        for solicitacao in solicitacoes:
            print(
                gradiente_texto(
                    f"{solicitacao.id_solicitacao:<5}{solicitacao.especificacao_tecnica[:33]:<35}{solicitacao.quantidade_solicitacao:<6}{solicitacao.status:<20}",
                    self.TURQUESA, self.TURQUESA_CLARO
                )
            )

        print()
        print(gradiente_texto(f"Total de solicitações: {len(solicitacoes)}", self.TURQUESA, self.TURQUESA_CLARO))
        print()
        input("Pressione ENTER para continuar...")

    def atualizar_status(self):
        print()
        print(gradiente_texto("=" * 60, self.TURQUESA_ESCURO, self.TURQUESA_CLARO))
        print(gradiente_texto("ATUALIZAR STATUS", self.TURQUESA, self.TURQUESA_CLARO))
        print(gradiente_texto("=" * 60, self.TURQUESA_CLARO, self.TURQUESA_ESCURO))

        try:
            id_solicitacao = int(
                input(gradiente_texto("Código da solicitação: ", self.TURQUESA_ESCURO, self.TURQUESA))
            )
            status = validar_status_compra(
                input(gradiente_texto(f"Novo status {STATUS_VALIDOS}: ", self.TURQUESA, self.TURQUESA_CLARO))
            )

        except ValueError as erro:
            print()
            print(gradiente_texto(f"Erro: {erro}", self.TURQUESA_CLARO, self.TURQUESA_ESCURO))
            input("\nPressione ENTER para continuar...")
            return

        self.repository.atualizar_status(id_solicitacao, status)
        print()
        input("Pressione ENTER para continuar...")

    def excluir_solicitacao(self):
        print()
        print(gradiente_texto("=" * 60, self.TURQUESA_ESCURO, self.TURQUESA_CLARO))
        print(gradiente_texto("EXCLUSÃO DE SOLICITAÇÃO", self.TURQUESA, self.TURQUESA_CLARO))
        print(gradiente_texto("=" * 60, self.TURQUESA_CLARO, self.TURQUESA_ESCURO))

        try:
            id_solicitacao = int(
                input(gradiente_texto("Código da solicitação: ", self.TURQUESA_ESCURO, self.TURQUESA))
            )

        except ValueError:
            print()
            print("Código inválido.")
            input("\nPressione ENTER para continuar...")
            return

        solicitacao = self.repository.buscar_por_id(id_solicitacao)

        if solicitacao is None:
            print()
            print("Solicitação não encontrada.")
            input("\nPressione ENTER para continuar...")
            return

        resposta = input(
            gradiente_texto("Deseja realmente excluir esta solicitação? (S/N): ", self.TURQUESA_CLARO, self.TURQUESA_ESCURO)
        ).strip().upper()

        if resposta != "S":
            print()
            print("Operação cancelada.")
            input("\nPressione ENTER para continuar...")
            return

        self.repository.excluir(id_solicitacao)
        print()
        input("Pressione ENTER para continuar...")
