from repositories.alerta_estoque_repository import AlertaEstoqueRepository

from menus.gradiente import gradiente_texto


class MenuAlertaEstoque:

    # Coral: vinho escuro -> coral -> rosa claro
    VINHO_ESCURO = (50, 10, 20)
    CORAL = (190, 55, 95)
    ROSA_CLARO = (240, 165, 185)

    def __init__(self):
        self.repository = AlertaEstoqueRepository()

    # submenu — alertas nascem automaticamente na baixa de estoque (ver
    # ItemAlmoxarifadoRepository.dar_baixa); aqui só se acompanha/resolve.
    def exibir(self):
        while True:
            print()
            print(gradiente_texto("=" * 60, self.VINHO_ESCURO, self.ROSA_CLARO))
            print(gradiente_texto("CTW MANUTENÇÃO - ALERTAS DE ESTOQUE", self.CORAL, self.ROSA_CLARO))
            print(gradiente_texto("=" * 60, self.ROSA_CLARO, self.VINHO_ESCURO))
            print(gradiente_texto("1 - Listar Alertas Pendentes", self.VINHO_ESCURO, self.CORAL))
            print(gradiente_texto("2 - Listar Todos os Alertas", self.CORAL, self.ROSA_CLARO))
            print(gradiente_texto("3 - Resolver Alerta", self.CORAL, self.ROSA_CLARO))
            print(gradiente_texto("4 - Excluir Alerta", self.VINHO_ESCURO, self.ROSA_CLARO))
            print(gradiente_texto("0 - Sair", self.VINHO_ESCURO, self.CORAL))
            print(gradiente_texto("=" * 60, self.ROSA_CLARO, self.VINHO_ESCURO))

            opcao = input(gradiente_texto("Escolha uma opção: ", self.ROSA_CLARO, self.VINHO_ESCURO))

            if opcao == "1":
                self.listar_pendentes()

            elif opcao == "2":
                self.listar_todos()

            elif opcao == "3":
                self.resolver_alerta()

            elif opcao == "4":
                self.excluir_alerta()

            elif opcao == "0":
                self.repository.fechar()
                print()
                print(gradiente_texto("Voltando ao menu principal...", self.VINHO_ESCURO, self.CORAL))
                break

            else:
                print()
                print(gradiente_texto("Opção inválida!", self.ROSA_CLARO, self.VINHO_ESCURO))

    def listar_pendentes(self):
        print()
        print(gradiente_texto("=" * 60, self.VINHO_ESCURO, self.ROSA_CLARO))
        print(gradiente_texto("ALERTAS PENDENTES", self.CORAL, self.ROSA_CLARO))
        print(gradiente_texto("=" * 60, self.ROSA_CLARO, self.VINHO_ESCURO))
        self._imprimir_lista(self.repository.listar_pendentes())

    def listar_todos(self):
        print()
        print(gradiente_texto("=" * 60, self.VINHO_ESCURO, self.ROSA_CLARO))
        print(gradiente_texto("TODOS OS ALERTAS", self.CORAL, self.ROSA_CLARO))
        print(gradiente_texto("=" * 60, self.ROSA_CLARO, self.VINHO_ESCURO))
        self._imprimir_lista(self.repository.listar())

    def _imprimir_lista(self, alertas):
        if not alertas:
            print()
            print("Nenhum alerta encontrado.")
            print()
            input("Pressione ENTER para continuar...")
            return

        print(
            gradiente_texto(
                f"{'ID':<5}{'Item (id)':<12}{'Mensagem':<40}{'Status':<12}",
                self.VINHO_ESCURO, self.ROSA_CLARO
            )
        )
        print(gradiente_texto("-" * 65, self.ROSA_CLARO, self.VINHO_ESCURO))

        for alerta in alertas:
            print(
                gradiente_texto(
                    f"{alerta.id_alerta:<5}{alerta.item_id:<12}{alerta.mensagem_alerta:<40}{alerta.status:<12}",
                    self.CORAL, self.ROSA_CLARO
                )
            )

        print()
        print(gradiente_texto(f"Total de alertas: {len(alertas)}", self.CORAL, self.ROSA_CLARO))
        print()
        input("Pressione ENTER para continuar...")

    def resolver_alerta(self):
        print()
        print(gradiente_texto("=" * 60, self.VINHO_ESCURO, self.ROSA_CLARO))
        print(gradiente_texto("RESOLVER ALERTA", self.CORAL, self.ROSA_CLARO))
        print(gradiente_texto("=" * 60, self.ROSA_CLARO, self.VINHO_ESCURO))

        try:
            id_alerta = int(
                input(gradiente_texto("Código do alerta: ", self.VINHO_ESCURO, self.CORAL))
            )

        except ValueError:
            print()
            print("Código inválido.")
            input("\nPressione ENTER para continuar...")
            return

        self.repository.resolver(id_alerta)
        print()
        input("Pressione ENTER para continuar...")

    def excluir_alerta(self):
        print()
        print(gradiente_texto("=" * 60, self.VINHO_ESCURO, self.ROSA_CLARO))
        print(gradiente_texto("EXCLUSÃO DE ALERTA", self.CORAL, self.ROSA_CLARO))
        print(gradiente_texto("=" * 60, self.ROSA_CLARO, self.VINHO_ESCURO))

        try:
            id_alerta = int(
                input(gradiente_texto("Código do alerta: ", self.VINHO_ESCURO, self.CORAL))
            )

        except ValueError:
            print()
            print("Código inválido.")
            input("\nPressione ENTER para continuar...")
            return

        alerta = self.repository.buscar_por_id(id_alerta)

        if alerta is None:
            print()
            print("Alerta não encontrado.")
            input("\nPressione ENTER para continuar...")
            return

        resposta = input(
            gradiente_texto("Deseja realmente excluir este alerta? (S/N): ", self.ROSA_CLARO, self.VINHO_ESCURO)
        ).strip().upper()

        if resposta != "S":
            print()
            print("Operação cancelada.")
            input("\nPressione ENTER para continuar...")
            return

        self.repository.excluir(id_alerta)
        print()
        input("Pressione ENTER para continuar...")
