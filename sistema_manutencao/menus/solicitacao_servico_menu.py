from models.solicitacao_servico import PRIORIDADES_VALIDAS, TIPOS_MANUTENCAO_VALIDOS, SolicitacaoServico
from repositories.solicitacao_servico_repository import (
    SolicitacaoServicoRepository,
    TransicaoInvalidaError,
)
from utils.solicitacao_servico_validacoes import (
    validar_descricao_problema,
    validar_prioridade_ss,
    validar_tipo_manutencao_ss,
)

from menus.gradiente import gradiente_texto


class MenuSolicitacaoServico:

    # Índigo: quase preto -> índigo -> lilás claro
    INDIGO_ESCURO = (18, 12, 50)
    INDIGO = (70, 50, 165)
    LILAS_CLARO = (185, 175, 230)

    def __init__(self):
        self.repository = SolicitacaoServicoRepository()

    # submenu
    def exibir(self):
        while True:
            print()
            print(gradiente_texto("=" * 60, self.INDIGO_ESCURO, self.LILAS_CLARO))
            print(gradiente_texto("CTW MANUTENÇÃO - SOLICITAÇÕES DE SERVIÇO", self.INDIGO, self.LILAS_CLARO))
            print(gradiente_texto("=" * 60, self.LILAS_CLARO, self.INDIGO_ESCURO))
            print(gradiente_texto("1 - Abrir Solicitação", self.INDIGO_ESCURO, self.INDIGO))
            print(gradiente_texto("2 - Buscar Solicitação", self.INDIGO_ESCURO, self.INDIGO))
            print(gradiente_texto("3 - Listar Solicitações", self.INDIGO, self.LILAS_CLARO))
            print(gradiente_texto("4 - Listar por Status", self.INDIGO, self.LILAS_CLARO))
            print(gradiente_texto("5 - Listar por Máquina", self.INDIGO, self.LILAS_CLARO))
            print(gradiente_texto("6 - Mudar Status", self.INDIGO_ESCURO, self.LILAS_CLARO))
            print(gradiente_texto("7 - Atribuir Responsável", self.INDIGO_ESCURO, self.LILAS_CLARO))
            print(gradiente_texto("8 - Excluir Solicitação", self.INDIGO_ESCURO, self.LILAS_CLARO))
            print(gradiente_texto("0 - Sair", self.INDIGO_ESCURO, self.INDIGO))
            print(gradiente_texto("=" * 60, self.LILAS_CLARO, self.INDIGO_ESCURO))

            opcao = input(gradiente_texto("Escolha uma opção: ", self.LILAS_CLARO, self.INDIGO_ESCURO))

            if opcao == "1":
                self.abrir_solicitacao()

            elif opcao == "2":
                self.buscar_solicitacao()

            elif opcao == "3":
                self.listar_solicitacao()

            elif opcao == "4":
                self.listar_por_status()

            elif opcao == "5":
                self.listar_por_maquina()

            elif opcao == "6":
                self.mudar_status()

            elif opcao == "7":
                self.atribuir_responsavel()

            elif opcao == "8":
                self.excluir_solicitacao()

            elif opcao == "0":
                self.repository.fechar()
                print()
                print(gradiente_texto("Voltando ao menu principal...", self.INDIGO_ESCURO, self.INDIGO))
                break

            else:
                print()
                print(gradiente_texto("Opção inválida!", self.LILAS_CLARO, self.INDIGO_ESCURO))

    def abrir_solicitacao(self):
        print()
        print(gradiente_texto("=" * 60, self.INDIGO_ESCURO, self.LILAS_CLARO))
        print(gradiente_texto("ABRIR SOLICITAÇÃO DE SERVIÇO", self.INDIGO, self.LILAS_CLARO))
        print(gradiente_texto("=" * 60, self.LILAS_CLARO, self.INDIGO_ESCURO))

        try:
            maquina_id = int(
                input(gradiente_texto("Código (id) da máquina: ", self.INDIGO_ESCURO, self.INDIGO))
            )
            solicitante_id = int(
                input(gradiente_texto("Código (id) do solicitante: ", self.INDIGO_ESCURO, self.INDIGO))
            )
            descricao_problema = validar_descricao_problema(
                input(gradiente_texto("Descrição do problema: ", self.INDIGO, self.LILAS_CLARO))
            )
            prioridade_ss = validar_prioridade_ss(
                input(gradiente_texto(f"Prioridade {PRIORIDADES_VALIDAS} [Média]: ", self.INDIGO, self.LILAS_CLARO)) or "Média"
            )
            tipo_manutencao = validar_tipo_manutencao_ss(
                input(gradiente_texto(f"Tipo {TIPOS_MANUTENCAO_VALIDOS} [Corretiva]: ", self.LILAS_CLARO, self.INDIGO_ESCURO)) or "Corretiva"
            )

        except ValueError as erro:
            print()
            print(gradiente_texto(f"Erro: {erro}", self.LILAS_CLARO, self.INDIGO_ESCURO))
            input("\nPressione ENTER para continuar...")
            return

        solicitacao = SolicitacaoServico(
            maquina_id=maquina_id,
            solicitante_id=solicitante_id,
            descricao_problema=descricao_problema,
            prioridade_ss=prioridade_ss,
            tipo_manutencao=tipo_manutencao
        )
        self.repository.salvar(solicitacao)
        print()
        input("Pressione ENTER para continuar...")

    def buscar_solicitacao(self):
        print()
        print(gradiente_texto("=" * 60, self.INDIGO_ESCURO, self.LILAS_CLARO))
        print(gradiente_texto("BUSCAR SOLICITAÇÃO", self.INDIGO, self.LILAS_CLARO))
        print(gradiente_texto("=" * 60, self.LILAS_CLARO, self.INDIGO_ESCURO))

        try:
            id_ss = int(
                input(gradiente_texto("Código da solicitação: ", self.INDIGO_ESCURO, self.INDIGO))
            )

        except ValueError:
            print()
            print("Código inválido.")
            input("\nPressione ENTER para continuar...")
            return

        solicitacao = self.repository.buscar_por_id(id_ss)
        print()

        if solicitacao is None:
            print("Solicitação não encontrada.")

        else:
            print(gradiente_texto(f"Código............: {solicitacao.id_ss}", self.INDIGO_ESCURO, self.INDIGO))
            print(gradiente_texto(f"Máquina (id)......: {solicitacao.maquina_id}", self.INDIGO, self.LILAS_CLARO))
            print(gradiente_texto(f"Solicitante (id)..: {solicitacao.solicitante_id}", self.LILAS_CLARO, self.INDIGO_ESCURO))
            print(gradiente_texto(f"Responsável (id)..: {solicitacao.responsavel_id}", self.INDIGO_ESCURO, self.INDIGO))
            print(gradiente_texto(f"Problema..........: {solicitacao.descricao_problema}", self.INDIGO, self.LILAS_CLARO))
            print(gradiente_texto(f"Prioridade........: {solicitacao.prioridade_ss}", self.LILAS_CLARO, self.INDIGO_ESCURO))
            print(gradiente_texto(f"Tipo..............: {solicitacao.tipo_manutencao}", self.INDIGO_ESCURO, self.INDIGO))
            print(gradiente_texto(f"Status............: {solicitacao.status}", self.INDIGO, self.LILAS_CLARO))

        print()
        input("Pressione ENTER para continuar...")

    def listar_solicitacao(self):
        print()
        print(gradiente_texto("=" * 60, self.INDIGO_ESCURO, self.LILAS_CLARO))
        print(gradiente_texto("LISTA DE SOLICITAÇÕES", self.INDIGO, self.LILAS_CLARO))
        print(gradiente_texto("=" * 60, self.LILAS_CLARO, self.INDIGO_ESCURO))
        self._imprimir_lista(self.repository.listar())

    def listar_por_status(self):
        print()
        print(gradiente_texto("=" * 60, self.INDIGO_ESCURO, self.LILAS_CLARO))
        print(gradiente_texto("SOLICITAÇÕES POR STATUS", self.INDIGO, self.LILAS_CLARO))
        print(gradiente_texto("=" * 60, self.LILAS_CLARO, self.INDIGO_ESCURO))
        status = input(gradiente_texto("Status: ", self.INDIGO_ESCURO, self.INDIGO))
        self._imprimir_lista(self.repository.listar_por_status(status))

    def listar_por_maquina(self):
        print()
        print(gradiente_texto("=" * 60, self.INDIGO_ESCURO, self.LILAS_CLARO))
        print(gradiente_texto("SOLICITAÇÕES POR MÁQUINA", self.INDIGO, self.LILAS_CLARO))
        print(gradiente_texto("=" * 60, self.LILAS_CLARO, self.INDIGO_ESCURO))

        try:
            maquina_id = int(
                input(gradiente_texto("Código (id) da máquina: ", self.INDIGO_ESCURO, self.INDIGO))
            )

        except ValueError:
            print()
            print("Código inválido.")
            input("\nPressione ENTER para continuar...")
            return

        self._imprimir_lista(self.repository.listar_por_maquina(maquina_id))

    def _imprimir_lista(self, solicitacoes):
        if not solicitacoes:
            print()
            print("Nenhuma solicitação encontrada.")
            print()
            input("Pressione ENTER para continuar...")
            return

        print(
            gradiente_texto(
                f"{'ID':<5}{'Máquina':<9}{'Problema':<30}{'Prioridade':<12}{'Status':<18}",
                self.INDIGO_ESCURO, self.LILAS_CLARO
            )
        )
        print(gradiente_texto("-" * 74, self.LILAS_CLARO, self.INDIGO_ESCURO))

        for solicitacao in solicitacoes:
            print(
                gradiente_texto(
                    f"{solicitacao.id_ss:<5}{solicitacao.maquina_id:<9}{solicitacao.descricao_problema[:28]:<30}{solicitacao.prioridade_ss:<12}{solicitacao.status:<18}",
                    self.INDIGO, self.LILAS_CLARO
                )
            )

        print()
        print(gradiente_texto(f"Total de solicitações: {len(solicitacoes)}", self.INDIGO, self.LILAS_CLARO))
        print()
        input("Pressione ENTER para continuar...")

    def mudar_status(self):
        print()
        print(gradiente_texto("=" * 60, self.INDIGO_ESCURO, self.LILAS_CLARO))
        print(gradiente_texto("MUDAR STATUS DA SOLICITAÇÃO", self.INDIGO, self.LILAS_CLARO))
        print(gradiente_texto("=" * 60, self.LILAS_CLARO, self.INDIGO_ESCURO))

        try:
            id_ss = int(
                input(gradiente_texto("Código da solicitação: ", self.INDIGO_ESCURO, self.INDIGO))
            )
            novo_status = input(
                gradiente_texto("Novo status: ", self.INDIGO, self.LILAS_CLARO)
            )
            self.repository.atualizar_status(id_ss, novo_status)

        except (ValueError, TransicaoInvalidaError) as erro:
            print()
            print(gradiente_texto(f"Erro: {erro}", self.LILAS_CLARO, self.INDIGO_ESCURO))

        print()
        input("Pressione ENTER para continuar...")

    def atribuir_responsavel(self):
        print()
        print(gradiente_texto("=" * 60, self.INDIGO_ESCURO, self.LILAS_CLARO))
        print(gradiente_texto("ATRIBUIR RESPONSÁVEL", self.INDIGO, self.LILAS_CLARO))
        print(gradiente_texto("=" * 60, self.LILAS_CLARO, self.INDIGO_ESCURO))

        try:
            id_ss = int(
                input(gradiente_texto("Código da solicitação: ", self.INDIGO_ESCURO, self.INDIGO))
            )
            responsavel_id = int(
                input(gradiente_texto("Código (id) do responsável: ", self.INDIGO, self.LILAS_CLARO))
            )

        except ValueError:
            print()
            print("Valor inválido.")
            input("\nPressione ENTER para continuar...")
            return

        self.repository.atribuir_responsavel(id_ss, responsavel_id)
        print()
        input("Pressione ENTER para continuar...")

    def excluir_solicitacao(self):
        print()
        print(gradiente_texto("=" * 60, self.INDIGO_ESCURO, self.LILAS_CLARO))
        print(gradiente_texto("EXCLUSÃO DE SOLICITAÇÃO", self.INDIGO, self.LILAS_CLARO))
        print(gradiente_texto("=" * 60, self.LILAS_CLARO, self.INDIGO_ESCURO))

        try:
            id_ss = int(
                input(gradiente_texto("Código da solicitação: ", self.INDIGO_ESCURO, self.INDIGO))
            )

        except ValueError:
            print()
            print("Código inválido.")
            input("\nPressione ENTER para continuar...")
            return

        solicitacao = self.repository.buscar_por_id(id_ss)

        if solicitacao is None:
            print()
            print("Solicitação não encontrada.")
            input("\nPressione ENTER para continuar...")
            return

        resposta = input(
            gradiente_texto("Deseja realmente excluir esta solicitação? (S/N): ", self.LILAS_CLARO, self.INDIGO_ESCURO)
        ).strip().upper()

        if resposta != "S":
            print()
            print("Operação cancelada.")
            input("\nPressione ENTER para continuar...")
            return

        self.repository.excluir(id_ss)
        print()
        input("Pressione ENTER para continuar...")
