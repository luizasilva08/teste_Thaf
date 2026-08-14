from repositories.log_auditoria_repository import LogAuditoriaRepository
from utils.log_auditoria_validacoes import validar_acao

from menus.gradiente import gradiente_texto


class MenuLogAuditoria:

    # Vermelho de alerta: vermelho escuro -> vermelho -> rosa claro
    VERMELHO_ESCURO = (40, 10, 10)
    VERMELHO = (150, 40, 40)
    ROSA_CLARO = (230, 170, 170)

    def __init__(self):
        self.repository = LogAuditoriaRepository()

    # submenu — somente registrar/listar, log de auditoria não é editável nem excluível (RN-003)
    def exibir(self):
        while True:
            print()
            print(gradiente_texto("=" * 60, self.VERMELHO_ESCURO, self.ROSA_CLARO))
            print(gradiente_texto("CTW MANUTENÇÃO - LOGS DE AUDITORIA", self.VERMELHO, self.ROSA_CLARO))
            print(gradiente_texto("=" * 60, self.ROSA_CLARO, self.VERMELHO_ESCURO))
            print(gradiente_texto("1 - Registrar Log", self.VERMELHO_ESCURO, self.VERMELHO))
            print(gradiente_texto("2 - Listar Todos os Logs", self.VERMELHO, self.ROSA_CLARO))
            print(gradiente_texto("3 - Listar Logs por Usuário", self.VERMELHO, self.ROSA_CLARO))
            print(gradiente_texto("0 - Sair", self.VERMELHO_ESCURO, self.VERMELHO))
            print(gradiente_texto("=" * 60, self.ROSA_CLARO, self.VERMELHO_ESCURO))

            opcao = input(gradiente_texto("Escolha uma opção: ", self.ROSA_CLARO, self.VERMELHO_ESCURO))

            if opcao == "1":
                self.registrar_log()

            elif opcao == "2":
                self.listar_log()

            elif opcao == "3":
                self.listar_log_por_usuario()

            elif opcao == "0":
                self.repository.fechar()
                print()
                print(gradiente_texto("Voltando ao menu principal...", self.VERMELHO_ESCURO, self.VERMELHO))
                break

            else:
                print()
                print(gradiente_texto("Opção inválida!", self.ROSA_CLARO, self.VERMELHO_ESCURO))

    def registrar_log(self):
        print()
        print(gradiente_texto("=" * 60, self.VERMELHO_ESCURO, self.ROSA_CLARO))
        print(gradiente_texto("REGISTRAR LOG DE AUDITORIA", self.VERMELHO, self.ROSA_CLARO))
        print(gradiente_texto("=" * 60, self.ROSA_CLARO, self.VERMELHO_ESCURO))

        try:
            usuario_id = int(
                input(gradiente_texto("Código (id) do usuário: ", self.VERMELHO_ESCURO, self.VERMELHO))
            )
            acao = validar_acao(
                input(gradiente_texto("Ação (ex: login, exclusão de perfil...): ", self.VERMELHO, self.ROSA_CLARO))
            )
            endereco_ip = input(
                gradiente_texto("Endereço IP (ENTER se não houver): ", self.ROSA_CLARO, self.VERMELHO_ESCURO)
            ) or None

        except ValueError as erro:
            print()
            print(gradiente_texto(f"Erro: {erro}", self.ROSA_CLARO, self.VERMELHO_ESCURO))
            input("\nPressione ENTER para continuar...")
            return

        self.repository.registrar(usuario_id, acao, endereco_ip)
        print()
        input("Pressione ENTER para continuar...")

    def listar_log(self):
        print()
        print(gradiente_texto("=" * 60, self.VERMELHO_ESCURO, self.ROSA_CLARO))
        print(gradiente_texto("LISTA DE LOGS DE AUDITORIA", self.VERMELHO, self.ROSA_CLARO))
        print(gradiente_texto("=" * 60, self.ROSA_CLARO, self.VERMELHO_ESCURO))
        self._imprimir_lista(self.repository.listar())

    def listar_log_por_usuario(self):
        print()
        print(gradiente_texto("=" * 60, self.VERMELHO_ESCURO, self.ROSA_CLARO))
        print(gradiente_texto("LOGS POR USUÁRIO", self.VERMELHO, self.ROSA_CLARO))
        print(gradiente_texto("=" * 60, self.ROSA_CLARO, self.VERMELHO_ESCURO))

        try:
            usuario_id = int(
                input(gradiente_texto("Código (id) do usuário: ", self.VERMELHO_ESCURO, self.VERMELHO))
            )

        except ValueError:
            print()
            print("Código inválido.")
            input("\nPressione ENTER para continuar...")
            return

        self._imprimir_lista(self.repository.listar_por_usuario(usuario_id))

    def _imprimir_lista(self, logs):
        if not logs:
            print()
            print("Nenhum log encontrado.")
            print()
            input("Pressione ENTER para continuar...")
            return

        print(
            gradiente_texto(
                f"{'ID':<5}{'Usuário':<10}{'Ação':<30}{'IP':<16}{'Data/hora':<20}",
                self.VERMELHO_ESCURO, self.ROSA_CLARO
            )
        )
        print(gradiente_texto("-" * 80, self.ROSA_CLARO, self.VERMELHO_ESCURO))

        for log in logs:
            print(
                gradiente_texto(
                    f"{log.id_log:<5}{log.usuario_id:<10}{log.acao:<30}{(log.endereco_ip or '-'):<16}{str(log.criado_em):<20}",
                    self.VERMELHO, self.ROSA_CLARO
                )
            )

        print()
        print(gradiente_texto(f"Total de logs: {len(logs)}", self.VERMELHO, self.ROSA_CLARO))
        print()
        input("Pressione ENTER para continuar...")
