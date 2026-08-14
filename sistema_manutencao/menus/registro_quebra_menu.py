from models.registro_quebra import RegistroQuebra
from repositories.registro_quebra_repository import RegistroQuebraRepository
from utils.registro_quebra_validacoes import validar_descricao_quebra

from menus.gradiente import gradiente_texto


class MenuRegistroQuebra:

    # Cinza grafite: quase preto -> cinza -> cinza claro
    GRAFITE_ESCURO = (18, 18, 18)
    CINZA = (90, 90, 90)
    CINZA_CLARO = (190, 190, 190)

    def __init__(self):
        self.repository = RegistroQuebraRepository()

    # submenu
    def exibir(self):
        while True:
            print()
            print(gradiente_texto("=" * 60, self.GRAFITE_ESCURO, self.CINZA_CLARO))
            print(gradiente_texto("CTW MANUTENÇÃO - REGISTRO DE QUEBRA", self.CINZA, self.CINZA_CLARO))
            print(gradiente_texto("=" * 60, self.CINZA_CLARO, self.GRAFITE_ESCURO))
            print(gradiente_texto("1 - Registrar Quebra", self.GRAFITE_ESCURO, self.CINZA))
            print(gradiente_texto("2 - Buscar Registro", self.GRAFITE_ESCURO, self.CINZA))
            print(gradiente_texto("3 - Listar Registros", self.CINZA, self.CINZA_CLARO))
            print(gradiente_texto("4 - Listar Registros por Item", self.CINZA, self.CINZA_CLARO))
            print(gradiente_texto("5 - Excluir Registro", self.GRAFITE_ESCURO, self.CINZA_CLARO))
            print(gradiente_texto("0 - Sair", self.GRAFITE_ESCURO, self.CINZA))
            print(gradiente_texto("=" * 60, self.CINZA_CLARO, self.GRAFITE_ESCURO))

            opcao = input(gradiente_texto("Escolha uma opção: ", self.CINZA_CLARO, self.GRAFITE_ESCURO))

            if opcao == "1":
                self.registrar_quebra()

            elif opcao == "2":
                self.buscar_registro()

            elif opcao == "3":
                self.listar_registro()

            elif opcao == "4":
                self.listar_registro_por_item()

            elif opcao == "5":
                self.excluir_registro()

            elif opcao == "0":
                self.repository.fechar()
                print()
                print(gradiente_texto("Voltando ao menu principal...", self.GRAFITE_ESCURO, self.CINZA))
                break

            else:
                print()
                print(gradiente_texto("Opção inválida!", self.CINZA_CLARO, self.GRAFITE_ESCURO))

    def registrar_quebra(self):
        print()
        print(gradiente_texto("=" * 60, self.GRAFITE_ESCURO, self.CINZA_CLARO))
        print(gradiente_texto("REGISTRAR QUEBRA", self.CINZA, self.CINZA_CLARO))
        print(gradiente_texto("=" * 60, self.CINZA_CLARO, self.GRAFITE_ESCURO))

        try:
            item_id = int(
                input(gradiente_texto("Código do item: ", self.GRAFITE_ESCURO, self.CINZA))
            )
            usuario_id = int(
                input(gradiente_texto("Código (id) do usuário: ", self.GRAFITE_ESCURO, self.CINZA))
            )
            descricao_quebra = validar_descricao_quebra(
                input(gradiente_texto("Descrição da quebra: ", self.CINZA, self.CINZA_CLARO))
            )
            foto_url = input(
                gradiente_texto("URL/caminho da foto (ENTER se não houver): ", self.CINZA_CLARO, self.GRAFITE_ESCURO)
            ) or None

        except ValueError as erro:
            print()
            print(gradiente_texto(f"Erro: {erro}", self.CINZA_CLARO, self.GRAFITE_ESCURO))
            input("\nPressione ENTER para continuar...")
            return

        registro = RegistroQuebra(
            item_id=item_id,
            usuario_id=usuario_id,
            descricao_quebra=descricao_quebra,
            foto_url=foto_url
        )
        self.repository.salvar(registro)
        print()
        input("Pressione ENTER para continuar...")

    def buscar_registro(self):
        print()
        print(gradiente_texto("=" * 60, self.GRAFITE_ESCURO, self.CINZA_CLARO))
        print(gradiente_texto("BUSCAR REGISTRO DE QUEBRA", self.CINZA, self.CINZA_CLARO))
        print(gradiente_texto("=" * 60, self.CINZA_CLARO, self.GRAFITE_ESCURO))

        try:
            id_quebra = int(
                input(gradiente_texto("Código do registro: ", self.GRAFITE_ESCURO, self.CINZA))
            )

        except ValueError:
            print()
            print("Código inválido.")
            input("\nPressione ENTER para continuar...")
            return

        registro = self.repository.buscar_por_id(id_quebra)
        print()

        if registro is None:
            print("Registro não encontrado.")

        else:
            print(gradiente_texto(f"Código......: {registro.id_quebra}", self.GRAFITE_ESCURO, self.CINZA))
            print(gradiente_texto(f"Item (id)...: {registro.item_id}", self.CINZA, self.CINZA_CLARO))
            print(gradiente_texto(f"Usuário (id): {registro.usuario_id}", self.CINZA_CLARO, self.GRAFITE_ESCURO))
            print(gradiente_texto(f"Descrição...: {registro.descricao_quebra}", self.GRAFITE_ESCURO, self.CINZA))
            print(gradiente_texto(f"Foto........: {registro.foto_url}", self.CINZA, self.CINZA_CLARO))

        print()
        input("Pressione ENTER para continuar...")

    def listar_registro(self):
        print()
        print(gradiente_texto("=" * 60, self.GRAFITE_ESCURO, self.CINZA_CLARO))
        print(gradiente_texto("LISTA DE REGISTROS DE QUEBRA", self.CINZA, self.CINZA_CLARO))
        print(gradiente_texto("=" * 60, self.CINZA_CLARO, self.GRAFITE_ESCURO))
        self._imprimir_lista(self.repository.listar())

    def listar_registro_por_item(self):
        print()
        print(gradiente_texto("=" * 60, self.GRAFITE_ESCURO, self.CINZA_CLARO))
        print(gradiente_texto("REGISTROS POR ITEM", self.CINZA, self.CINZA_CLARO))
        print(gradiente_texto("=" * 60, self.CINZA_CLARO, self.GRAFITE_ESCURO))

        try:
            item_id = int(
                input(gradiente_texto("Código do item: ", self.GRAFITE_ESCURO, self.CINZA))
            )

        except ValueError:
            print()
            print("Código inválido.")
            input("\nPressione ENTER para continuar...")
            return

        self._imprimir_lista(self.repository.listar_por_item(item_id))

    def _imprimir_lista(self, registros):
        if not registros:
            print()
            print("Nenhum registro encontrado.")
            print()
            input("Pressione ENTER para continuar...")
            return

        print(
            gradiente_texto(
                f"{'ID':<5}{'Item':<8}{'Usuário':<10}{'Descrição':<30}",
                self.GRAFITE_ESCURO, self.CINZA_CLARO
            )
        )
        print(gradiente_texto("-" * 55, self.CINZA_CLARO, self.GRAFITE_ESCURO))

        for registro in registros:
            print(
                gradiente_texto(
                    f"{registro.id_quebra:<5}{registro.item_id:<8}{registro.usuario_id:<10}{registro.descricao_quebra:<30}",
                    self.CINZA, self.CINZA_CLARO
                )
            )

        print()
        print(gradiente_texto(f"Total de registros: {len(registros)}", self.CINZA, self.CINZA_CLARO))
        print()
        input("Pressione ENTER para continuar...")

    def excluir_registro(self):
        print()
        print(gradiente_texto("=" * 60, self.GRAFITE_ESCURO, self.CINZA_CLARO))
        print(gradiente_texto("EXCLUSÃO DE REGISTRO", self.CINZA, self.CINZA_CLARO))
        print(gradiente_texto("=" * 60, self.CINZA_CLARO, self.GRAFITE_ESCURO))

        try:
            id_quebra = int(
                input(gradiente_texto("Código do registro: ", self.GRAFITE_ESCURO, self.CINZA))
            )

        except ValueError:
            print()
            print("Código inválido.")
            input("\nPressione ENTER para continuar...")
            return

        registro = self.repository.buscar_por_id(id_quebra)

        if registro is None:
            print()
            print("Registro não encontrado.")
            input("\nPressione ENTER para continuar...")
            return

        resposta = input(
            gradiente_texto("Deseja realmente excluir este registro? (S/N): ", self.CINZA_CLARO, self.GRAFITE_ESCURO)
        ).strip().upper()

        if resposta != "S":
            print()
            print("Operação cancelada.")
            input("\nPressione ENTER para continuar...")
            return

        self.repository.excluir(id_quebra)
        print()
        input("Pressione ENTER para continuar...")
