from models.item_almoxarifado import ItemAlmoxarifado
from repositories.item_almoxarifado_repository import ItemAlmoxarifadoRepository
from utils.item_almoxarifado_validacoes import validar_nome_ferramenta, validar_quantidade

from menus.gradiente import gradiente_texto


class MenuItemAlmoxarifado:

    # Marrom couro: marrom escuro -> marrom -> bege claro
    MARROM_ESCURO = (35, 22, 12)
    MARROM = (130, 85, 45)
    BEGE_CLARO = (210, 175, 130)

    def __init__(self):
        self.repository = ItemAlmoxarifadoRepository()

    # submenu
    def exibir(self):
        while True:
            print()
            print(gradiente_texto("=" * 60, self.MARROM_ESCURO, self.BEGE_CLARO))
            print(gradiente_texto("CTW MANUTENÇÃO - ALMOXARIFADO", self.MARROM, self.BEGE_CLARO))
            print(gradiente_texto("=" * 60, self.BEGE_CLARO, self.MARROM_ESCURO))
            print(gradiente_texto("1 - Cadastrar Item", self.MARROM_ESCURO, self.MARROM))
            print(gradiente_texto("2 - Buscar Item", self.MARROM_ESCURO, self.MARROM))
            print(gradiente_texto("3 - Listar Itens", self.MARROM, self.BEGE_CLARO))
            print(gradiente_texto("4 - Itens Abaixo do Mínimo", self.MARROM, self.BEGE_CLARO))
            print(gradiente_texto("5 - Dar Entrada em Estoque", self.MARROM, self.BEGE_CLARO))
            print(gradiente_texto("6 - Dar Baixa em Estoque", self.MARROM_ESCURO, self.BEGE_CLARO))
            print(gradiente_texto("7 - Atualizar Item", self.MARROM_ESCURO, self.BEGE_CLARO))
            print(gradiente_texto("8 - Excluir Item", self.MARROM_ESCURO, self.BEGE_CLARO))
            print(gradiente_texto("0 - Sair", self.MARROM_ESCURO, self.MARROM))
            print(gradiente_texto("=" * 60, self.BEGE_CLARO, self.MARROM_ESCURO))

            opcao = input(gradiente_texto("Escolha uma opção: ", self.BEGE_CLARO, self.MARROM_ESCURO))

            if opcao == "1":
                self.cadastrar_item()

            elif opcao == "2":
                self.buscar_item()

            elif opcao == "3":
                self.listar_item()

            elif opcao == "4":
                self.listar_abaixo_do_minimo()

            elif opcao == "5":
                self.dar_entrada()

            elif opcao == "6":
                self.dar_baixa()

            elif opcao == "7":
                self.atualizar_item()

            elif opcao == "8":
                self.excluir_item()

            elif opcao == "0":
                self.repository.fechar()
                print()
                print(gradiente_texto("Voltando ao menu principal...", self.MARROM_ESCURO, self.MARROM))
                break

            else:
                print()
                print(gradiente_texto("Opção inválida!", self.BEGE_CLARO, self.MARROM_ESCURO))

    def cadastrar_item(self):
        print()
        print(gradiente_texto("=" * 60, self.MARROM_ESCURO, self.BEGE_CLARO))
        print(gradiente_texto("CADASTRO DE ITEM", self.MARROM, self.BEGE_CLARO))
        print(gradiente_texto("=" * 60, self.BEGE_CLARO, self.MARROM_ESCURO))

        try:
            nome_ferramenta = validar_nome_ferramenta(
                input(gradiente_texto("Nome do item: ", self.MARROM_ESCURO, self.MARROM))
            )
            dimensao_ferramenta = input(gradiente_texto("Dimensão (ex: 1/2 pol, ENTER se não houver): ", self.MARROM, self.BEGE_CLARO)) or None
            quantidade_atual = validar_quantidade(
                int(input(gradiente_texto("Quantidade inicial [0]: ", self.MARROM, self.BEGE_CLARO)) or 0),
                "quantidade inicial"
            )
            estoque_minimo = validar_quantidade(
                int(input(gradiente_texto("Estoque mínimo [1]: ", self.BEGE_CLARO, self.MARROM_ESCURO)) or 1),
                "estoque mínimo"
            )
            unidade_medida = input(gradiente_texto("Unidade (UN/PÇ/KG) [UN]: ", self.BEGE_CLARO, self.MARROM_ESCURO)) or "UN"
            localizacao_gaveta = input(gradiente_texto("Localização (gaveta/prateleira): ", self.MARROM_ESCURO, self.MARROM)) or None

        except ValueError as erro:
            print()
            print(gradiente_texto(f"Erro: {erro}", self.BEGE_CLARO, self.MARROM_ESCURO))
            input("\nPressione ENTER para continuar...")
            return

        item = ItemAlmoxarifado(
            nome_ferramenta=nome_ferramenta,
            dimensao_ferramenta=dimensao_ferramenta,
            quantidade_atual=quantidade_atual,
            estoque_minimo=estoque_minimo,
            unidade_medida=unidade_medida,
            localizacao_gaveta=localizacao_gaveta
        )
        self.repository.salvar(item)
        print()
        input("Pressione ENTER para continuar...")

    def buscar_item(self):
        print()
        print(gradiente_texto("=" * 60, self.MARROM_ESCURO, self.BEGE_CLARO))
        print(gradiente_texto("BUSCAR ITEM", self.MARROM, self.BEGE_CLARO))
        print(gradiente_texto("=" * 60, self.BEGE_CLARO, self.MARROM_ESCURO))

        try:
            id_ferramenta = int(
                input(gradiente_texto("Código do item: ", self.MARROM_ESCURO, self.MARROM))
            )

        except ValueError:
            print()
            print("Código inválido.")
            input("\nPressione ENTER para continuar...")
            return

        item = self.repository.buscar_por_id(id_ferramenta)
        print()

        if item is None:
            print("Item não encontrado.")

        else:
            print(gradiente_texto(f"Código..........: {item.id_ferramenta}", self.MARROM_ESCURO, self.MARROM))
            print(gradiente_texto(f"Nome............: {item.nome_ferramenta}", self.MARROM, self.BEGE_CLARO))
            print(gradiente_texto(f"Dimensão........: {item.dimensao_ferramenta}", self.BEGE_CLARO, self.MARROM_ESCURO))
            print(gradiente_texto(f"Quantidade......: {item.quantidade_atual} {item.unidade_medida}", self.MARROM_ESCURO, self.MARROM))
            print(gradiente_texto(f"Estoque mínimo..: {item.estoque_minimo}", self.MARROM, self.BEGE_CLARO))
            print(gradiente_texto(f"Localização.....: {item.localizacao_gaveta}", self.BEGE_CLARO, self.MARROM_ESCURO))

        print()
        input("Pressione ENTER para continuar...")

    def listar_item(self):
        print()
        print(gradiente_texto("=" * 60, self.MARROM_ESCURO, self.BEGE_CLARO))
        print(gradiente_texto("LISTA DE ITENS", self.MARROM, self.BEGE_CLARO))
        print(gradiente_texto("=" * 60, self.BEGE_CLARO, self.MARROM_ESCURO))
        self._imprimir_lista(self.repository.listar())

    def listar_abaixo_do_minimo(self):
        print()
        print(gradiente_texto("=" * 60, self.MARROM_ESCURO, self.BEGE_CLARO))
        print(gradiente_texto("ITENS ABAIXO DO MÍNIMO", self.MARROM, self.BEGE_CLARO))
        print(gradiente_texto("=" * 60, self.BEGE_CLARO, self.MARROM_ESCURO))
        self._imprimir_lista(self.repository.listar_abaixo_do_minimo())

    def _imprimir_lista(self, itens):
        if not itens:
            print()
            print("Nenhum item encontrado.")
            print()
            input("Pressione ENTER para continuar...")
            return

        print(
            gradiente_texto(
                f"{'ID':<5}{'Nome':<25}{'Qtd':<10}{'Mín':<6}{'UN':<5}",
                self.MARROM_ESCURO, self.BEGE_CLARO
            )
        )
        print(gradiente_texto("-" * 55, self.BEGE_CLARO, self.MARROM_ESCURO))

        for item in itens:
            print(
                gradiente_texto(
                    f"{item.id_ferramenta:<5}{item.nome_ferramenta:<25}{item.quantidade_atual:<10}{item.estoque_minimo:<6}{item.unidade_medida:<5}",
                    self.MARROM, self.BEGE_CLARO
                )
            )

        print()
        print(gradiente_texto(f"Total de itens: {len(itens)}", self.MARROM, self.BEGE_CLARO))
        print()
        input("Pressione ENTER para continuar...")

    def dar_entrada(self):
        print()
        print(gradiente_texto("=" * 60, self.MARROM_ESCURO, self.BEGE_CLARO))
        print(gradiente_texto("ENTRADA DE ESTOQUE", self.MARROM, self.BEGE_CLARO))
        print(gradiente_texto("=" * 60, self.BEGE_CLARO, self.MARROM_ESCURO))

        try:
            id_ferramenta = int(
                input(gradiente_texto("Código do item: ", self.MARROM_ESCURO, self.MARROM))
            )
            quantidade = int(
                input(gradiente_texto("Quantidade a entrar: ", self.MARROM, self.BEGE_CLARO))
            )

        except ValueError:
            print()
            print("Valor inválido.")
            input("\nPressione ENTER para continuar...")
            return

        self.repository.dar_entrada(id_ferramenta, quantidade)
        print()
        input("Pressione ENTER para continuar...")

    def dar_baixa(self):
        print()
        print(gradiente_texto("=" * 60, self.MARROM_ESCURO, self.BEGE_CLARO))
        print(gradiente_texto("BAIXA DE ESTOQUE", self.MARROM, self.BEGE_CLARO))
        print(gradiente_texto("=" * 60, self.BEGE_CLARO, self.MARROM_ESCURO))

        try:
            id_ferramenta = int(
                input(gradiente_texto("Código do item: ", self.MARROM_ESCURO, self.MARROM))
            )
            quantidade = int(
                input(gradiente_texto("Quantidade a baixar: ", self.MARROM, self.BEGE_CLARO))
            )

        except ValueError:
            print()
            print("Valor inválido.")
            input("\nPressione ENTER para continuar...")
            return

        item = self.repository.dar_baixa(id_ferramenta, quantidade)
        if item is not None and item.quantidade_atual < item.estoque_minimo:
            print(gradiente_texto("ATENÇÃO: item abaixo do estoque mínimo — alerta gerado.", self.BEGE_CLARO, self.MARROM_ESCURO))
        print()
        input("Pressione ENTER para continuar...")

    def atualizar_item(self):
        print()
        print(gradiente_texto("=" * 60, self.MARROM_ESCURO, self.BEGE_CLARO))
        print(gradiente_texto("ATUALIZAÇÃO DE ITEM", self.MARROM, self.BEGE_CLARO))
        print(gradiente_texto("=" * 60, self.BEGE_CLARO, self.MARROM_ESCURO))

        try:
            id_ferramenta = int(
                input(gradiente_texto("Código do item: ", self.MARROM_ESCURO, self.MARROM))
            )

        except ValueError:
            print()
            print("Código inválido.")
            input("\nPressione ENTER para continuar...")
            return

        item = self.repository.buscar_por_id(id_ferramenta)

        if item is None:
            print()
            print("Item não encontrado.")
            input("\nPressione ENTER para continuar...")
            return

        print()
        print(gradiente_texto("Pressione ENTER para manter o valor atual.", self.MARROM, self.BEGE_CLARO))
        print()

        nome_ferramenta = input(
            gradiente_texto(f"Nome [{item.nome_ferramenta}]: ", self.MARROM_ESCURO, self.MARROM)
        )
        if nome_ferramenta:
            try:
                item.nome_ferramenta = validar_nome_ferramenta(nome_ferramenta)
            except ValueError as erro:
                print(gradiente_texto(f"Erro: {erro}", self.BEGE_CLARO, self.MARROM_ESCURO))
                input("\nPressione ENTER para continuar...")
                return

        estoque_minimo = input(
            gradiente_texto(f"Estoque mínimo [{item.estoque_minimo}]: ", self.MARROM, self.BEGE_CLARO)
        )
        if estoque_minimo:
            item.estoque_minimo = int(estoque_minimo)

        localizacao_gaveta = input(
            gradiente_texto(f"Localização [{item.localizacao_gaveta}]: ", self.BEGE_CLARO, self.MARROM_ESCURO)
        )
        if localizacao_gaveta:
            item.localizacao_gaveta = localizacao_gaveta

        self.repository.atualizar(item)
        print()
        input("Pressione ENTER para continuar...")

    def excluir_item(self):
        print()
        print(gradiente_texto("=" * 60, self.MARROM_ESCURO, self.BEGE_CLARO))
        print(gradiente_texto("EXCLUSÃO DE ITEM", self.MARROM, self.BEGE_CLARO))
        print(gradiente_texto("=" * 60, self.BEGE_CLARO, self.MARROM_ESCURO))

        try:
            id_ferramenta = int(
                input(gradiente_texto("Código do item: ", self.MARROM_ESCURO, self.MARROM))
            )

        except ValueError:
            print()
            print("Código inválido.")
            input("\nPressione ENTER para continuar...")
            return

        item = self.repository.buscar_por_id(id_ferramenta)

        if item is None:
            print()
            print("Item não encontrado.")
            input("\nPressione ENTER para continuar...")
            return

        print()
        print(gradiente_texto("Item localizado", self.MARROM, self.BEGE_CLARO))
        print(gradiente_texto("-" * 60, self.BEGE_CLARO, self.MARROM_ESCURO))
        print(gradiente_texto(f"Código.....: {item.id_ferramenta}", self.MARROM_ESCURO, self.MARROM))
        print(gradiente_texto(f"Nome.......: {item.nome_ferramenta}", self.MARROM, self.BEGE_CLARO))
        print()

        resposta = input(
            gradiente_texto("Deseja realmente excluir este item? (S/N): ", self.BEGE_CLARO, self.MARROM_ESCURO)
        ).strip().upper()

        if resposta != "S":
            print()
            print("Operação cancelada.")
            input("\nPressione ENTER para continuar...")
            return

        self.repository.excluir(id_ferramenta)
        print()
        input("Pressione ENTER para continuar...")
