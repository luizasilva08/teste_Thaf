from datetime import datetime

from models.calendario_preventivo import FREQUENCIAS_VALIDAS, CalendarioPreventivo
from repositories.calendario_preventivo_repository import CalendarioPreventivoRepository
from utils.calendario_preventivo_validacoes import (
    validar_data_execucao,
    validar_frequencia,
    validar_titulo_calendario,
)

from menus.gradiente import gradiente_texto


class MenuCalendarioPreventivo:

    # Magenta: vinho escuro -> magenta -> lilás rosado claro
    VINHO_ESCURO = (40, 10, 35)
    MAGENTA = (160, 50, 140)
    LILAS_ROSA = (225, 160, 215)

    def __init__(self):
        self.repository = CalendarioPreventivoRepository()

    # submenu
    def exibir(self):
        while True:
            print()
            print(gradiente_texto("=" * 60, self.VINHO_ESCURO, self.LILAS_ROSA))
            print(gradiente_texto("CTW MANUTENÇÃO - CALENDÁRIO PREVENTIVO", self.MAGENTA, self.LILAS_ROSA))
            print(gradiente_texto("=" * 60, self.LILAS_ROSA, self.VINHO_ESCURO))
            print(gradiente_texto("1 - Agendar Preventiva", self.VINHO_ESCURO, self.MAGENTA))
            print(gradiente_texto("2 - Buscar Agendamento", self.VINHO_ESCURO, self.MAGENTA))
            print(gradiente_texto("3 - Listar Agendamentos", self.MAGENTA, self.LILAS_ROSA))
            print(gradiente_texto("4 - Listar por Período", self.MAGENTA, self.LILAS_ROSA))
            print(gradiente_texto("5 - Listar Atrasadas", self.MAGENTA, self.LILAS_ROSA))
            print(gradiente_texto("6 - Concluir e Reagendar", self.VINHO_ESCURO, self.LILAS_ROSA))
            print(gradiente_texto("7 - Excluir Agendamento", self.VINHO_ESCURO, self.LILAS_ROSA))
            print(gradiente_texto("0 - Sair", self.VINHO_ESCURO, self.MAGENTA))
            print(gradiente_texto("=" * 60, self.LILAS_ROSA, self.VINHO_ESCURO))

            opcao = input(gradiente_texto("Escolha uma opção: ", self.LILAS_ROSA, self.VINHO_ESCURO))

            if opcao == "1":
                self.agendar()

            elif opcao == "2":
                self.buscar_agendamento()

            elif opcao == "3":
                self.listar_agendamento()

            elif opcao == "4":
                self.listar_por_periodo()

            elif opcao == "5":
                self.listar_atrasadas()

            elif opcao == "6":
                self.concluir_e_reagendar()

            elif opcao == "7":
                self.excluir_agendamento()

            elif opcao == "0":
                self.repository.fechar()
                print()
                print(gradiente_texto("Voltando ao menu principal...", self.VINHO_ESCURO, self.MAGENTA))
                break

            else:
                print()
                print(gradiente_texto("Opção inválida!", self.LILAS_ROSA, self.VINHO_ESCURO))

    def agendar(self):
        print()
        print(gradiente_texto("=" * 60, self.VINHO_ESCURO, self.LILAS_ROSA))
        print(gradiente_texto("AGENDAR PREVENTIVA", self.MAGENTA, self.LILAS_ROSA))
        print(gradiente_texto("=" * 60, self.LILAS_ROSA, self.VINHO_ESCURO))

        try:
            maquina_id = int(
                input(gradiente_texto("Código (id) da máquina: ", self.VINHO_ESCURO, self.MAGENTA))
            )
            titulo_calendario = validar_titulo_calendario(
                input(gradiente_texto("Título: ", self.MAGENTA, self.LILAS_ROSA))
            )
            frequencia_calendario = validar_frequencia(
                input(gradiente_texto(f"Frequência {FREQUENCIAS_VALIDAS}: ", self.LILAS_ROSA, self.VINHO_ESCURO))
            )
            data_proxima_execucao = validar_data_execucao(
                input(gradiente_texto("Próxima execução (AAAA-MM-DD): ", self.VINHO_ESCURO, self.MAGENTA))
            )

        except ValueError as erro:
            print()
            print(gradiente_texto(f"Erro: {erro}", self.LILAS_ROSA, self.VINHO_ESCURO))
            input("\nPressione ENTER para continuar...")
            return

        calendario = CalendarioPreventivo(
            maquina_id=maquina_id,
            titulo_calendario=titulo_calendario,
            frequencia_calendario=frequencia_calendario,
            data_proxima_execucao=data_proxima_execucao
        )
        self.repository.salvar(calendario)
        print()
        input("Pressione ENTER para continuar...")

    def buscar_agendamento(self):
        print()
        print(gradiente_texto("=" * 60, self.VINHO_ESCURO, self.LILAS_ROSA))
        print(gradiente_texto("BUSCAR AGENDAMENTO", self.MAGENTA, self.LILAS_ROSA))
        print(gradiente_texto("=" * 60, self.LILAS_ROSA, self.VINHO_ESCURO))

        try:
            id_calendario = int(
                input(gradiente_texto("Código do agendamento: ", self.VINHO_ESCURO, self.MAGENTA))
            )

        except ValueError:
            print()
            print("Código inválido.")
            input("\nPressione ENTER para continuar...")
            return

        calendario = self.repository.buscar_por_id(id_calendario)
        print()

        if calendario is None:
            print("Agendamento não encontrado.")

        else:
            print(gradiente_texto(f"Código............: {calendario.id_calendario}", self.VINHO_ESCURO, self.MAGENTA))
            print(gradiente_texto(f"Título............: {calendario.titulo_calendario}", self.MAGENTA, self.LILAS_ROSA))
            print(gradiente_texto(f"Máquina (id)......: {calendario.maquina_id}", self.LILAS_ROSA, self.VINHO_ESCURO))
            print(gradiente_texto(f"Frequência........: {calendario.frequencia_calendario}", self.VINHO_ESCURO, self.MAGENTA))
            print(gradiente_texto(f"Próxima execução..: {calendario.data_proxima_execucao}", self.MAGENTA, self.LILAS_ROSA))
            print(gradiente_texto(f"Status............: {calendario.status}", self.LILAS_ROSA, self.VINHO_ESCURO))

        print()
        input("Pressione ENTER para continuar...")

    def listar_agendamento(self):
        print()
        print(gradiente_texto("=" * 60, self.VINHO_ESCURO, self.LILAS_ROSA))
        print(gradiente_texto("LISTA DE AGENDAMENTOS", self.MAGENTA, self.LILAS_ROSA))
        print(gradiente_texto("=" * 60, self.LILAS_ROSA, self.VINHO_ESCURO))
        self._imprimir_lista(self.repository.listar())

    def listar_por_periodo(self):
        print()
        print(gradiente_texto("=" * 60, self.VINHO_ESCURO, self.LILAS_ROSA))
        print(gradiente_texto("AGENDAMENTOS POR PERÍODO", self.MAGENTA, self.LILAS_ROSA))
        print(gradiente_texto("=" * 60, self.LILAS_ROSA, self.VINHO_ESCURO))

        try:
            inicio = datetime.strptime(
                input(gradiente_texto("Data início (AAAA-MM-DD): ", self.VINHO_ESCURO, self.MAGENTA)), "%Y-%m-%d"
            ).date()
            fim = datetime.strptime(
                input(gradiente_texto("Data fim (AAAA-MM-DD): ", self.MAGENTA, self.LILAS_ROSA)), "%Y-%m-%d"
            ).date()

        except ValueError:
            print()
            print("Data inválida.")
            input("\nPressione ENTER para continuar...")
            return

        self._imprimir_lista(self.repository.listar_por_periodo(inicio, fim))

    def listar_atrasadas(self):
        print()
        print(gradiente_texto("=" * 60, self.VINHO_ESCURO, self.LILAS_ROSA))
        print(gradiente_texto("AGENDAMENTOS ATRASADOS", self.MAGENTA, self.LILAS_ROSA))
        print(gradiente_texto("=" * 60, self.LILAS_ROSA, self.VINHO_ESCURO))
        self.repository.marcar_atrasadas()
        self._imprimir_lista(self.repository.listar_atrasadas())

    def _imprimir_lista(self, calendarios):
        if not calendarios:
            print()
            print("Nenhum agendamento encontrado.")
            print()
            input("Pressione ENTER para continuar...")
            return

        print(
            gradiente_texto(
                f"{'ID':<5}{'Título':<25}{'Máquina':<9}{'Frequência':<12}{'Próx. execução':<16}{'Status':<12}",
                self.VINHO_ESCURO, self.LILAS_ROSA
            )
        )
        print(gradiente_texto("-" * 79, self.LILAS_ROSA, self.VINHO_ESCURO))

        for calendario in calendarios:
            print(
                gradiente_texto(
                    f"{calendario.id_calendario:<5}{calendario.titulo_calendario[:23]:<25}{calendario.maquina_id:<9}{calendario.frequencia_calendario:<12}{str(calendario.data_proxima_execucao):<16}{calendario.status:<12}",
                    self.MAGENTA, self.LILAS_ROSA
                )
            )

        print()
        print(gradiente_texto(f"Total de agendamentos: {len(calendarios)}", self.MAGENTA, self.LILAS_ROSA))
        print()
        input("Pressione ENTER para continuar...")

    def concluir_e_reagendar(self):
        print()
        print(gradiente_texto("=" * 60, self.VINHO_ESCURO, self.LILAS_ROSA))
        print(gradiente_texto("CONCLUIR E REAGENDAR", self.MAGENTA, self.LILAS_ROSA))
        print(gradiente_texto("=" * 60, self.LILAS_ROSA, self.VINHO_ESCURO))

        try:
            id_calendario = int(
                input(gradiente_texto("Código do agendamento: ", self.VINHO_ESCURO, self.MAGENTA))
            )

        except ValueError:
            print()
            print("Código inválido.")
            input("\nPressione ENTER para continuar...")
            return

        self.repository.marcar_concluida(id_calendario)
        print()
        input("Pressione ENTER para continuar...")

    def excluir_agendamento(self):
        print()
        print(gradiente_texto("=" * 60, self.VINHO_ESCURO, self.LILAS_ROSA))
        print(gradiente_texto("EXCLUSÃO DE AGENDAMENTO", self.MAGENTA, self.LILAS_ROSA))
        print(gradiente_texto("=" * 60, self.LILAS_ROSA, self.VINHO_ESCURO))

        try:
            id_calendario = int(
                input(gradiente_texto("Código do agendamento: ", self.VINHO_ESCURO, self.MAGENTA))
            )

        except ValueError:
            print()
            print("Código inválido.")
            input("\nPressione ENTER para continuar...")
            return

        calendario = self.repository.buscar_por_id(id_calendario)

        if calendario is None:
            print()
            print("Agendamento não encontrado.")
            input("\nPressione ENTER para continuar...")
            return

        resposta = input(
            gradiente_texto("Deseja realmente excluir este agendamento? (S/N): ", self.LILAS_ROSA, self.VINHO_ESCURO)
        ).strip().upper()

        if resposta != "S":
            print()
            print("Operação cancelada.")
            input("\nPressione ENTER para continuar...")
            return

        self.repository.excluir(id_calendario)
        print()
        input("Pressione ENTER para continuar...")
