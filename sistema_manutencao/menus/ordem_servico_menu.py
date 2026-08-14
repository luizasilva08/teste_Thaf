from models.ordem_servico import CRITICIDADES_VALIDAS, TIPOS_MANUTENCAO_VALIDOS, OrdemServico
from repositories.ordem_servico_repository import OrdemServicoRepository
from utils.ordem_servico_validacoes import (
    validar_criticidade_os,
    validar_data,
    validar_descricao_execucao,
    validar_hora,
    validar_tipo_manutencao_os,
)

from menus.gradiente import gradiente_texto


class MenuOrdemServico:

    # Bronze/dourado: marrom escuro -> bronze -> dourado claro
    BRONZE_ESCURO = (45, 30, 5)
    BRONZE = (175, 130, 25)
    DOURADO_CLARO = (230, 200, 120)

    def __init__(self):
        self.repository = OrdemServicoRepository()

    # submenu
    def exibir(self):
        while True:
            print()
            print(gradiente_texto("=" * 60, self.BRONZE_ESCURO, self.DOURADO_CLARO))
            print(gradiente_texto("CTW MANUTENÇÃO - ORDENS DE SERVIÇO", self.BRONZE, self.DOURADO_CLARO))
            print(gradiente_texto("=" * 60, self.DOURADO_CLARO, self.BRONZE_ESCURO))
            print(gradiente_texto("1 - Concluir SS Abrindo uma OS", self.BRONZE_ESCURO, self.BRONZE))
            print(gradiente_texto("2 - Buscar OS", self.BRONZE_ESCURO, self.BRONZE))
            print(gradiente_texto("3 - Listar OS", self.BRONZE, self.DOURADO_CLARO))
            print(gradiente_texto("4 - Listar OS por Máquina", self.BRONZE, self.DOURADO_CLARO))
            print(gradiente_texto("5 - Excluir OS", self.BRONZE_ESCURO, self.DOURADO_CLARO))
            print(gradiente_texto("0 - Sair", self.BRONZE_ESCURO, self.BRONZE))
            print(gradiente_texto("=" * 60, self.DOURADO_CLARO, self.BRONZE_ESCURO))

            opcao = input(gradiente_texto("Escolha uma opção: ", self.DOURADO_CLARO, self.BRONZE_ESCURO))

            if opcao == "1":
                self.abrir_a_partir_de_ss()

            elif opcao == "2":
                self.buscar_ordem()

            elif opcao == "3":
                self.listar_ordem()

            elif opcao == "4":
                self.listar_por_maquina()

            elif opcao == "5":
                self.excluir_ordem()

            elif opcao == "0":
                self.repository.fechar()
                print()
                print(gradiente_texto("Voltando ao menu principal...", self.BRONZE_ESCURO, self.BRONZE))
                break

            else:
                print()
                print(gradiente_texto("Opção inválida!", self.DOURADO_CLARO, self.BRONZE_ESCURO))

    def abrir_a_partir_de_ss(self):
        print()
        print(gradiente_texto("=" * 60, self.BRONZE_ESCURO, self.DOURADO_CLARO))
        print(gradiente_texto("REGISTRAR EXECUÇÃO (OS)", self.BRONZE, self.DOURADO_CLARO))
        print(gradiente_texto("=" * 60, self.DOURADO_CLARO, self.BRONZE_ESCURO))

        try:
            solicitacao_id = int(
                input(gradiente_texto("Código da SS a concluir: ", self.BRONZE_ESCURO, self.BRONZE))
            )
            tipo_manutencao = validar_tipo_manutencao_os(
                input(gradiente_texto(f"Tipo {TIPOS_MANUTENCAO_VALIDOS}: ", self.BRONZE, self.DOURADO_CLARO))
            )
            criticidade_os = validar_criticidade_os(
                input(gradiente_texto(f"Criticidade {CRITICIDADES_VALIDAS}: ", self.DOURADO_CLARO, self.BRONZE_ESCURO))
            )
            descricao_execucao = validar_descricao_execucao(
                input(gradiente_texto("Descrição da execução: ", self.BRONZE_ESCURO, self.BRONZE))
            )
            pecas_usadas = input(gradiente_texto("Peças usadas (ENTER se não houver): ", self.BRONZE, self.DOURADO_CLARO)) or None
            data_execucao = validar_data(
                input(gradiente_texto("Data de execução (AAAA-MM-DD): ", self.DOURADO_CLARO, self.BRONZE_ESCURO))
            )
            hora_inicio = validar_hora(
                input(gradiente_texto("Hora início (HH:MM): ", self.BRONZE_ESCURO, self.BRONZE)), "hora início"
            )
            hora_fim = validar_hora(
                input(gradiente_texto("Hora fim (HH:MM): ", self.BRONZE, self.DOURADO_CLARO)), "hora fim"
            )
            quantidade_pessoas = int(input(gradiente_texto("Quantidade de pessoas [1]: ", self.DOURADO_CLARO, self.BRONZE_ESCURO)) or 1)

            self.repository.abrir_a_partir_de_ss(
                solicitacao_id=solicitacao_id,
                tipo_manutencao=tipo_manutencao,
                criticidade_os=criticidade_os,
                descricao_execucao=descricao_execucao,
                pecas_usadas=pecas_usadas,
                data_execucao=data_execucao,
                hora_inicio=hora_inicio,
                hora_fim=hora_fim,
                quantidade_pessoas=quantidade_pessoas
            )
            print()
            print(gradiente_texto("OS registrada. SS concluída e máquina marcada como 'Operando'.", self.BRONZE, self.DOURADO_CLARO))

        except ValueError as erro:
            print()
            print(gradiente_texto(f"Erro: {erro}", self.DOURADO_CLARO, self.BRONZE_ESCURO))

        print()
        input("Pressione ENTER para continuar...")

    def buscar_ordem(self):
        print()
        print(gradiente_texto("=" * 60, self.BRONZE_ESCURO, self.DOURADO_CLARO))
        print(gradiente_texto("BUSCAR OS", self.BRONZE, self.DOURADO_CLARO))
        print(gradiente_texto("=" * 60, self.DOURADO_CLARO, self.BRONZE_ESCURO))

        try:
            id_os = int(
                input(gradiente_texto("Código da OS: ", self.BRONZE_ESCURO, self.BRONZE))
            )

        except ValueError:
            print()
            print("Código inválido.")
            input("\nPressione ENTER para continuar...")
            return

        ordem = self.repository.buscar_por_id(id_os)
        print()

        if ordem is None:
            print("OS não encontrada.")

        else:
            print(gradiente_texto(f"Código............: {ordem.id_os}", self.BRONZE_ESCURO, self.BRONZE))
            print(gradiente_texto(f"Solicitação (id)..: {ordem.solicitacao_id}", self.BRONZE, self.DOURADO_CLARO))
            print(gradiente_texto(f"Máquina (id)......: {ordem.maquina_id}", self.DOURADO_CLARO, self.BRONZE_ESCURO))
            print(gradiente_texto(f"Tipo..............: {ordem.tipo_manutencao}", self.BRONZE_ESCURO, self.BRONZE))
            print(gradiente_texto(f"Criticidade.......: {ordem.criticidade_os}", self.BRONZE, self.DOURADO_CLARO))
            print(gradiente_texto(f"Execução..........: {ordem.data_execucao} {ordem.hora_inicio}-{ordem.hora_fim}", self.DOURADO_CLARO, self.BRONZE_ESCURO))
            print(gradiente_texto(f"Descrição.........: {ordem.descricao_execucao}", self.BRONZE_ESCURO, self.BRONZE))

        print()
        input("Pressione ENTER para continuar...")

    def listar_ordem(self):
        print()
        print(gradiente_texto("=" * 60, self.BRONZE_ESCURO, self.DOURADO_CLARO))
        print(gradiente_texto("LISTA DE OS", self.BRONZE, self.DOURADO_CLARO))
        print(gradiente_texto("=" * 60, self.DOURADO_CLARO, self.BRONZE_ESCURO))
        self._imprimir_lista(self.repository.listar())

    def listar_por_maquina(self):
        print()
        print(gradiente_texto("=" * 60, self.BRONZE_ESCURO, self.DOURADO_CLARO))
        print(gradiente_texto("OS POR MÁQUINA", self.BRONZE, self.DOURADO_CLARO))
        print(gradiente_texto("=" * 60, self.DOURADO_CLARO, self.BRONZE_ESCURO))

        try:
            maquina_id = int(
                input(gradiente_texto("Código (id) da máquina: ", self.BRONZE_ESCURO, self.BRONZE))
            )

        except ValueError:
            print()
            print("Código inválido.")
            input("\nPressione ENTER para continuar...")
            return

        self._imprimir_lista(self.repository.listar_por_maquina(maquina_id))

    def _imprimir_lista(self, ordens):
        if not ordens:
            print()
            print("Nenhuma OS encontrada.")
            print()
            input("Pressione ENTER para continuar...")
            return

        print(
            gradiente_texto(
                f"{'ID':<5}{'SS':<6}{'Máquina':<9}{'Tipo':<14}{'Criticidade':<12}{'Data':<12}",
                self.BRONZE_ESCURO, self.DOURADO_CLARO
            )
        )
        print(gradiente_texto("-" * 58, self.DOURADO_CLARO, self.BRONZE_ESCURO))

        for ordem in ordens:
            print(
                gradiente_texto(
                    f"{ordem.id_os:<5}{ordem.solicitacao_id:<6}{ordem.maquina_id:<9}{ordem.tipo_manutencao:<14}{ordem.criticidade_os:<12}{str(ordem.data_execucao):<12}",
                    self.BRONZE, self.DOURADO_CLARO
                )
            )

        print()
        print(gradiente_texto(f"Total de OS: {len(ordens)}", self.BRONZE, self.DOURADO_CLARO))
        print()
        input("Pressione ENTER para continuar...")

    def excluir_ordem(self):
        print()
        print(gradiente_texto("=" * 60, self.BRONZE_ESCURO, self.DOURADO_CLARO))
        print(gradiente_texto("EXCLUSÃO DE OS", self.BRONZE, self.DOURADO_CLARO))
        print(gradiente_texto("=" * 60, self.DOURADO_CLARO, self.BRONZE_ESCURO))

        try:
            id_os = int(
                input(gradiente_texto("Código da OS: ", self.BRONZE_ESCURO, self.BRONZE))
            )

        except ValueError:
            print()
            print("Código inválido.")
            input("\nPressione ENTER para continuar...")
            return

        ordem = self.repository.buscar_por_id(id_os)

        if ordem is None:
            print()
            print("OS não encontrada.")
            input("\nPressione ENTER para continuar...")
            return

        resposta = input(
            gradiente_texto("Deseja realmente excluir esta OS? (S/N): ", self.DOURADO_CLARO, self.BRONZE_ESCURO)
        ).strip().upper()

        if resposta != "S":
            print()
            print("Operação cancelada.")
            input("\nPressione ENTER para continuar...")
            return

        self.repository.excluir(id_os)
        print()
        input("Pressione ENTER para continuar...")
