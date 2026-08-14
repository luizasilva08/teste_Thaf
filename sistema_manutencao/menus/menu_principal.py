from menus.gradiente import gradiente_texto
from menus.perfil_menu import MenuPerfil
from menus.turma_menu import MenuTurma
from menus.usuario_menu import MenuUsuario
from menus.log_auditoria_menu import MenuLogAuditoria
from menus.setor_menu import MenuSetor
from menus.maquina_menu import MenuMaquina
from menus.item_almoxarifado_menu import MenuItemAlmoxarifado
from menus.alerta_estoque_menu import MenuAlertaEstoque
from menus.registro_quebra_menu import MenuRegistroQuebra
from menus.solicitacao_servico_menu import MenuSolicitacaoServico
from menus.ordem_servico_menu import MenuOrdemServico
from menus.solicitacao_compra_menu import MenuSolicitacaoCompra
from menus.calendario_preventivo_menu import MenuCalendarioPreventivo


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
            print(gradiente_texto("3 - Usuários", self.AZUL_MARINHO, self.AZUL_ACO))
            print(gradiente_texto("4 - Logs de Auditoria", self.AZUL_MARINHO, self.AZUL_ACO))
            print(gradiente_texto("5 - Setores", self.AZUL_MARINHO, self.AZUL_ACO))
            print(gradiente_texto("6 - Máquinas", self.AZUL_MARINHO, self.AZUL_ACO))
            print(gradiente_texto("7 - Almoxarifado (Itens)", self.AZUL_MARINHO, self.AZUL_ACO))
            print(gradiente_texto("8 - Alertas de Estoque", self.AZUL_MARINHO, self.AZUL_ACO))
            print(gradiente_texto("9 - Registro de Quebra", self.AZUL_MARINHO, self.AZUL_ACO))
            print(gradiente_texto("10 - Solicitações de Serviço (SS)", self.AZUL_MARINHO, self.AZUL_ACO))
            print(gradiente_texto("11 - Ordens de Serviço (OS)", self.AZUL_MARINHO, self.AZUL_ACO))
            print(gradiente_texto("12 - Solicitações de Compra", self.AZUL_MARINHO, self.AZUL_ACO))
            print(gradiente_texto("13 - Calendário Preventivo", self.AZUL_MARINHO, self.AZUL_ACO))
            print(gradiente_texto("0 - Sair", self.AZUL_MARINHO, self.AZUL_ACO))
            print(gradiente_texto("=" * 60, self.AZUL_CLARO, self.AZUL_MARINHO))

            opcao = input(gradiente_texto("Escolha uma opção: ", self.AZUL_CLARO, self.AZUL_MARINHO))

            if opcao == "1":
                MenuPerfil().exibir()

            elif opcao == "2":
                MenuTurma().exibir()

            elif opcao == "3":
                MenuUsuario().exibir()

            elif opcao == "4":
                MenuLogAuditoria().exibir()

            elif opcao == "5":
                MenuSetor().exibir()

            elif opcao == "6":
                MenuMaquina().exibir()

            elif opcao == "7":
                MenuItemAlmoxarifado().exibir()

            elif opcao == "8":
                MenuAlertaEstoque().exibir()

            elif opcao == "9":
                MenuRegistroQuebra().exibir()

            elif opcao == "10":
                MenuSolicitacaoServico().exibir()

            elif opcao == "11":
                MenuOrdemServico().exibir()

            elif opcao == "12":
                MenuSolicitacaoCompra().exibir()

            elif opcao == "13":
                MenuCalendarioPreventivo().exibir()

            elif opcao == "0":
                print()
                print(gradiente_texto("Sistema Encerrado", self.AZUL_MARINHO, self.AZUL_ACO))
                break

            else:
                print()
                print(gradiente_texto("Opção inválida!", self.AZUL_CLARO, self.AZUL_MARINHO))
