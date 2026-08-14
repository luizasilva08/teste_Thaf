from menus.gradiente import gradiente_texto
from menus.perfil_menu import MenuPerfil
from menus.turma_menu import MenuTurma


class MenuPrincipal:

    # Azul institucional: azul-marinho -> azul de aço -> azul claro
    AZUL_MARINHO = (10, 30, 60)
    AZUL_ACO = (40, 90, 160)
    AZUL_CLARO = (150, 195, 235)

    def exibir(self):
        while True:
            print()
            print(gradiente_texto("=" * 60, self.AZUL_MARINHO, self.AZUL_CLARO))
            print(gradiente_texto("CTW MANUTENÇÃO - MENU PRINCIPAL", self.AZUL_ACO, self.AZUL_CLARO))
            print(gradiente_texto("=" * 60, self.AZUL_CLARO, self.AZUL_MARINHO))
            print(gradiente_texto("1 - Perfis", self.AZUL_MARINHO, self.AZUL_ACO))
            print(gradiente_texto("2 - Turmas", self.AZUL_MARINHO, self.AZUL_ACO))
            print(gradiente_texto("0 - Sair", self.AZUL_MARINHO, self.AZUL_ACO))
            print(gradiente_texto("=" * 60, self.AZUL_CLARO, self.AZUL_MARINHO))

            opcao = input(gradiente_texto("Escolha uma opção: ", self.AZUL_CLARO, self.AZUL_MARINHO))

            if opcao == "1":
                MenuPerfil().exibir()

            elif opcao == "2":
                MenuTurma().exibir()

            elif opcao == "0":
                print()
                print(gradiente_texto("Sistema Encerrado", self.AZUL_MARINHO, self.AZUL_ACO))
                break

            else:
                print()
                print(gradiente_texto("Opção inválida!", self.AZUL_CLARO, self.AZUL_MARINHO))
