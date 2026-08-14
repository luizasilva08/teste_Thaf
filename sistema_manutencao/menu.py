"""Menu de linha de comando do Sistema de Gerenciamento de Manutenção (CTW)."""

from datetime import date, datetime

from models.calendario_preventivo import FREQUENCIAS_VALIDAS, CalendarioPreventivo
from models.maquina import STATUS_VALIDOS as STATUS_MAQUINA_VALIDOS
from models.maquina import Maquina
from models.ordem_servico import CRITICIDADES_VALIDAS
from models.ordem_servico import TIPOS_MANUTENCAO_VALIDOS as TIPOS_OS_VALIDOS
from models.perfil import PERFIS_VALIDOS, Perfil
from models.registro_quebra import RegistroQuebra
from models.setor import Setor
from models.solicitacao_compra import STATUS_VALIDOS as STATUS_COMPRA_VALIDOS
from models.solicitacao_compra import SolicitacaoCompra
from models.solicitacao_servico import PRIORIDADES_VALIDAS
from models.solicitacao_servico import TIPOS_MANUTENCAO_VALIDOS as TIPOS_SS_VALIDOS
from models.solicitacao_servico import SolicitacaoServico
from models.turma import Turma
from models.usuario import Usuario
from repositories.alerta_estoque_repository import AlertaEstoqueRepository
from repositories.calendario_preventivo_repository import CalendarioPreventivoRepository
from models.item_almoxarifado import ItemAlmoxarifado
from repositories.item_almoxarifado_repository import ItemAlmoxarifadoRepository
from repositories.log_auditoria_repository import LogAuditoriaRepository
from repositories.maquina_repository import MaquinaRepository
from repositories.ordem_servico_repository import OrdemServicoRepository
from repositories.perfil_repository import PerfilRepository
from repositories.registro_quebra_repository import RegistroQuebraRepository
from repositories.setor_repository import SetorRepository
from repositories.solicitacao_compra_repository import SolicitacaoCompraRepository
from repositories.solicitacao_servico_repository import (
    SolicitacaoServicoRepository,
    TransicaoInvalidaError,
)
from repositories.turma_repository import TurmaRepository
from repositories.usuario_repository import UsuarioRepository
from utils.validacoes import (
    ValidacaoError,
    exige_perfil,
    gerar_hash_senha,
    validar_campo_obrigatorio,
    validar_email,
    validar_opcao,
    verificar_senha,
)

usuario_logado: Usuario | None = None
perfil_logado: str | None = None


def entrada(mensagem: str) -> str:
    return input(mensagem).strip()


def pausar():
    input("\nPressione ENTER para continuar...")


# --------------------------------------------------------------------------
# Autenticação
# --------------------------------------------------------------------------

def fazer_login() -> bool:
    global usuario_logado, perfil_logado

    print("\n=== LOGIN ===")
    email = entrada("Email: ")
    senha = entrada("Senha: ")

    usuario = UsuarioRepository().buscar_por_email(email)
    if usuario is None or not verificar_senha(senha, usuario.senha_hash):
        print("Credenciais inválidas.")
        return False

    perfil = PerfilRepository().buscar_por_id(usuario.perfil_id)
    usuario_logado = usuario
    perfil_logado = perfil.nome if perfil else None

    LogAuditoriaRepository().registrar(usuario.id, "login")
    print(f"Bem-vindo(a), {usuario.nome} ({perfil_logado}).")
    return True


# --------------------------------------------------------------------------
# CRUD genérico para cadastros simples (perfis, turmas, setores, máquinas...)
# --------------------------------------------------------------------------

def menu_crud_perfis():
    repo = PerfilRepository()
    while True:
        print("\n--- Perfis --- (1) Listar (2) Criar (3) Editar (4) Excluir (0) Voltar")
        opcao = entrada("Opção: ")
        if opcao == "1":
            for p in repo.listar():
                print(p)
        elif opcao == "2":
            try:
                nome = validar_opcao(entrada("Nome (coordenador/gestor/professor/aluno/representante): ").lower(), PERFIS_VALIDOS, "nome")
                descricao = entrada("Descrição: ")
                novo_id = repo.criar(Perfil(nome=nome, descricao=descricao))
                print(f"Perfil criado com id {novo_id}.")
            except ValidacaoError as erro:
                print(f"Erro: {erro}")
        elif opcao == "3":
            id_ = int(entrada("ID do perfil: "))
            atual = repo.buscar_por_id(id_)
            if not atual:
                print("Não encontrado.")
                continue
            atual.descricao = entrada(f"Nova descrição [{atual.descricao}]: ") or atual.descricao
            repo.atualizar(id_, atual)
            print("Atualizado.")
        elif opcao == "4":
            id_ = int(entrada("ID do perfil: "))
            print("Excluído." if repo.excluir(id_) else "Não encontrado.")
        elif opcao == "0":
            return


def menu_crud_turmas():
    repo = TurmaRepository()
    while True:
        print("\n--- Turmas --- (1) Listar (2) Criar (3) Editar (4) Excluir (0) Voltar")
        opcao = entrada("Opção: ")
        if opcao == "1":
            for t in repo.listar():
                print(t)
        elif opcao == "2":
            codigo = entrada("Código (ex: MAN-2026-2T): ")
            periodo = entrada("Período: ")
            novo_id = repo.criar(Turma(codigo=codigo, periodo=periodo))
            print(f"Turma criada com id {novo_id}.")
        elif opcao == "3":
            id_ = int(entrada("ID da turma: "))
            atual = repo.buscar_por_id(id_)
            if not atual:
                print("Não encontrada.")
                continue
            atual.periodo = entrada(f"Novo período [{atual.periodo}]: ") or atual.periodo
            repo.atualizar(id_, atual)
            print("Atualizada.")
        elif opcao == "4":
            id_ = int(entrada("ID da turma: "))
            print("Excluída." if repo.excluir(id_) else "Não encontrada.")
        elif opcao == "0":
            return


def menu_crud_usuarios():
    exige_perfil(perfil_logado, ("coordenador", "gestor", "professor"))
    repo = UsuarioRepository()
    while True:
        print("\n--- Usuários --- (1) Listar (2) Criar (3) Excluir (0) Voltar")
        opcao = entrada("Opção: ")
        if opcao == "1":
            for u in repo.listar():
                print(f"{u.id} | {u.nome} | {u.email} | perfil={u.perfil_id} turma={u.turma_id}")
        elif opcao == "2":
            try:
                nome = validar_campo_obrigatorio(entrada("Nome: "), "nome")
                email = validar_email(entrada("Email: "))
                senha = entrada("Senha: ")
                perfil_id = int(entrada("ID do perfil: "))
                turma_id_str = entrada("ID da turma (ENTER se não houver): ")
                turma_id = int(turma_id_str) if turma_id_str else None
                novo_id = repo.criar(
                    Usuario(
                        perfil_id=perfil_id,
                        turma_id=turma_id,
                        nome=nome,
                        email=email,
                        senha_hash=gerar_hash_senha(senha),
                    )
                )
                print(f"Usuário criado com id {novo_id}.")
            except ValidacaoError as erro:
                print(f"Erro: {erro}")
        elif opcao == "3":
            id_ = int(entrada("ID do usuário: "))
            print("Excluído." if repo.excluir(id_) else "Não encontrado.")
        elif opcao == "0":
            return


def menu_crud_setores():
    repo = SetorRepository()
    while True:
        print("\n--- Setores --- (1) Listar (2) Criar (3) Excluir (0) Voltar")
        opcao = entrada("Opção: ")
        if opcao == "1":
            for s in repo.listar():
                print(s)
        elif opcao == "2":
            nome = entrada("Nome do setor: ")
            descricao = entrada("Descrição: ")
            novo_id = repo.criar(Setor(nome=nome, descricao=descricao))
            print(f"Setor criado com id {novo_id}.")
        elif opcao == "3":
            id_ = int(entrada("ID do setor: "))
            print("Excluído." if repo.excluir(id_) else "Não encontrado.")
        elif opcao == "0":
            return


def menu_crud_maquinas():
    repo = MaquinaRepository()
    while True:
        print("\n--- Máquinas --- (1) Listar (2) Criar (3) Atualizar status (4) Excluir (0) Voltar")
        opcao = entrada("Opção: ")
        if opcao == "1":
            for m in repo.listar():
                print(f"{m.id} | {m.tag} | {m.nome} | {m.status_vivo} | setor={m.setor_id}")
        elif opcao == "2":
            setor_id = int(entrada("ID do setor: "))
            tag = entrada("Tag (ex: TOR-01): ")
            nome = entrada("Nome da máquina: ")
            novo_id = repo.criar(Maquina(setor_id=setor_id, tag=tag, nome=nome))
            print(f"Máquina criada com id {novo_id}.")
        elif opcao == "3":
            id_ = int(entrada("ID da máquina: "))
            try:
                status = validar_opcao(entrada(f"Status {STATUS_MAQUINA_VALIDOS}: "), STATUS_MAQUINA_VALIDOS, "status")
                repo.atualizar_status(id_, status)
                print("Status atualizado.")
            except ValidacaoError as erro:
                print(f"Erro: {erro}")
        elif opcao == "4":
            id_ = int(entrada("ID da máquina: "))
            print("Excluída." if repo.excluir(id_) else "Não encontrada.")
        elif opcao == "0":
            return


# --------------------------------------------------------------------------
# Almoxarifado / Ferramentaria / Registro de Quebra
# --------------------------------------------------------------------------

def menu_almoxarifado():
    repo = ItemAlmoxarifadoRepository()
    while True:
        print("\n--- Almoxarifado --- (1) Listar (2) Cadastrar item (3) Entrada de estoque "
              "(4) Baixa de estoque (5) Itens abaixo do mínimo (0) Voltar")
        opcao = entrada("Opção: ")
        if opcao == "1":
            for i in repo.listar():
                print(f"{i.id} | {i.nome} | qtd={i.quantidade_atual}/{i.estoque_minimo} {i.unidade_medida}")
        elif opcao == "2":
            nome = entrada("Nome do item: ")
            quantidade = int(entrada("Quantidade inicial: ") or 0)
            minimo = int(entrada("Estoque mínimo: ") or 1)
            unidade = entrada("Unidade (UN/PÇ/KG) [UN]: ") or "UN"
            novo_id = repo.criar(
                ItemAlmoxarifado(
                    nome=nome, quantidade_atual=quantidade, estoque_minimo=minimo, unidade_medida=unidade
                )
            )
            print(f"Item criado com id {novo_id}.")
        elif opcao == "3":
            id_ = int(entrada("ID do item: "))
            quantidade = int(entrada("Quantidade a entrar: "))
            item = repo.dar_entrada(id_, quantidade)
            print(f"Novo saldo: {item.quantidade_atual}")
        elif opcao == "4":
            id_ = int(entrada("ID do item: "))
            quantidade = int(entrada("Quantidade a baixar: "))
            item = repo.dar_baixa(id_, quantidade)
            print(f"Novo saldo: {item.quantidade_atual}")
            if item.quantidade_atual < item.estoque_minimo:
                print("ATENÇÃO: item abaixo do estoque mínimo — alerta gerado.")
        elif opcao == "5":
            for i in repo.listar_abaixo_do_minimo():
                print(f"{i.id} | {i.nome} | qtd={i.quantidade_atual}/{i.estoque_minimo}")
        elif opcao == "0":
            return


def menu_alertas_estoque():
    repo = AlertaEstoqueRepository()
    while True:
        print("\n--- Alertas de Estoque --- (1) Listar pendentes (2) Resolver (0) Voltar")
        opcao = entrada("Opção: ")
        if opcao == "1":
            for a in repo.listar_pendentes():
                print(f"{a.id} | item={a.item_id} | {a.mensagem}")
        elif opcao == "2":
            id_ = int(entrada("ID do alerta: "))
            print("Resolvido." if repo.resolver(id_) else "Não encontrado.")
        elif opcao == "0":
            return


def menu_registro_quebra():
    repo = RegistroQuebraRepository()
    while True:
        print("\n--- Registro de Quebra de Ferramenta/Item --- (1) Registrar (2) Listar por item (0) Voltar")
        opcao = entrada("Opção: ")
        if opcao == "1":
            item_id = int(entrada("ID do item: "))
            descricao = entrada("Descrição da quebra: ")
            foto_url = entrada("URL/caminho da foto (opcional): ") or None
            novo_id = repo.criar(
                RegistroQuebra(
                    item_id=item_id,
                    usuario_id=usuario_logado.id,
                    descricao=descricao,
                    foto_url=foto_url,
                )
            )
            print(f"Registro criado com id {novo_id}.")
        elif opcao == "2":
            item_id = int(entrada("ID do item: "))
            for r in repo.listar_por_item(item_id):
                print(f"{r.id} | usuario={r.usuario_id} | {r.descricao} | {r.criado_em}")
        elif opcao == "0":
            return


# --------------------------------------------------------------------------
# Solicitação de Serviço (S.S.) e Ordem de Serviço (O.S.)
# --------------------------------------------------------------------------

def menu_ss_os():
    ss_repo = SolicitacaoServicoRepository()
    os_repo = OrdemServicoRepository()
    while True:
        print("\n--- SS / OS --- (1) Abrir SS (2) Listar SS por status (3) Mudar status da SS "
              "(4) Abrir OS a partir de SS concluindo o atendimento (0) Voltar")
        opcao = entrada("Opção: ")
        if opcao == "1":
            maquina_id = int(entrada("ID da máquina: "))
            descricao = entrada("Descrição do problema: ")
            prioridade = validar_opcao(entrada(f"Prioridade {PRIORIDADES_VALIDAS} [Média]: ") or "Média", PRIORIDADES_VALIDAS, "prioridade")
            tipo = validar_opcao(entrada(f"Tipo {TIPOS_SS_VALIDOS} [Corretiva]: ") or "Corretiva", TIPOS_SS_VALIDOS, "tipo")
            novo_id = ss_repo.criar(
                SolicitacaoServico(
                    maquina_id=maquina_id,
                    solicitante_id=usuario_logado.id,
                    descricao_problema=descricao,
                    prioridade_ss=prioridade,
                    tipo_manutencao=tipo,
                )
            )
            print(f"SS aberta com id {novo_id}.")
        elif opcao == "2":
            status = entrada("Status: ")
            for s in ss_repo.listar_por_status(status):
                print(f"{s.id} | máquina={s.maquina_id} | {s.descricao_problema[:40]} | {s.status}")
        elif opcao == "3":
            id_ = int(entrada("ID da SS: "))
            novo_status = entrada("Novo status: ")
            try:
                ss_repo.atualizar_status(id_, novo_status)
                print("Status atualizado.")
            except TransicaoInvalidaError as erro:
                print(f"Erro: {erro}")
        elif opcao == "4":
            solicitacao_id = int(entrada("ID da SS a concluir: "))
            try:
                tipo = validar_opcao(entrada(f"Tipo da OS {TIPOS_OS_VALIDOS}: "), TIPOS_OS_VALIDOS, "tipo")
                criticidade = validar_opcao(entrada(f"Criticidade {CRITICIDADES_VALIDAS}: "), CRITICIDADES_VALIDAS, "criticidade")
                descricao_execucao = entrada("Descrição da execução: ")
                pecas = entrada("Peças usadas (opcional): ") or None
                data_str = entrada("Data de execução (AAAA-MM-DD) [hoje]: ") or date.today().isoformat()
                inicio = entrada("Hora início (HH:MM): ")
                fim = entrada("Hora fim (HH:MM): ")
                pessoas = int(entrada("Quantidade de pessoas [1]: ") or 1)

                ss_repo.atualizar_status(solicitacao_id, "Validação")
                ss_repo.atualizar_status(solicitacao_id, "Concluída")

                novo_id = os_repo.abrir_a_partir_de_ss(
                    solicitacao_id,
                    tipo_manutencao=tipo,
                    criticidade=criticidade,
                    descricao_execucao=descricao_execucao,
                    pecas_usadas=pecas,
                    data_execucao=datetime.strptime(data_str, "%Y-%m-%d").date(),
                    hora_inicio=inicio,
                    hora_fim=fim,
                    quantidade_pessoas=pessoas,
                    turma_id=None,
                )
                print(f"OS criada com id {novo_id}. Máquina marcada como 'Operando'.")
            except (ValidacaoError, TransicaoInvalidaError, ValueError) as erro:
                print(f"Erro: {erro}")
        elif opcao == "0":
            return


# --------------------------------------------------------------------------
# Solicitação de Compras
# --------------------------------------------------------------------------

def menu_compras():
    repo = SolicitacaoCompraRepository()
    while True:
        print("\n--- Solicitação de Compras --- (1) Abrir (2) Listar por status (3) Atualizar status (0) Voltar")
        opcao = entrada("Opção: ")
        if opcao == "1":
            professor_id = int(entrada("ID do professor responsável: "))
            especificacao = entrada("Especificação técnica: ")
            justificativa = entrada("Justificativa: ")
            quantidade = int(entrada("Quantidade [1]: ") or 1)
            equipamento = entrada("Equipamento (opcional): ") or None
            novo_id = repo.criar(
                SolicitacaoCompra(
                    solicitante_id=usuario_logado.id,
                    professor_responsavel_id=professor_id,
                    especificacao_tecnica=especificacao,
                    justificativa=justificativa,
                    quantidade=quantidade,
                    equipamento=equipamento,
                )
            )
            print(f"Solicitação de compra criada com id {novo_id}.")
        elif opcao == "2":
            status = validar_opcao(entrada(f"Status {STATUS_COMPRA_VALIDOS}: "), STATUS_COMPRA_VALIDOS, "status")
            for c in repo.listar_por_status(status):
                print(f"{c.id} | {c.especificacao_tecnica[:40]} | qtd={c.quantidade} | {c.status}")
        elif opcao == "3":
            id_ = int(entrada("ID da solicitação: "))
            status = validar_opcao(entrada(f"Novo status {STATUS_COMPRA_VALIDOS}: "), STATUS_COMPRA_VALIDOS, "status")
            print("Atualizado." if repo.atualizar_status(id_, status) else "Não encontrada.")
        elif opcao == "0":
            return


# --------------------------------------------------------------------------
# Calendário Preventivo
# --------------------------------------------------------------------------

def menu_calendario_preventivo():
    repo = CalendarioPreventivoRepository()
    while True:
        print("\n--- Calendário Preventivo --- (1) Agendar (2) Listar por período "
              "(3) Concluir e reagendar (4) Listar atrasadas (0) Voltar")
        opcao = entrada("Opção: ")
        if opcao == "1":
            maquina_id = int(entrada("ID da máquina: "))
            titulo = entrada("Título: ")
            frequencia = validar_opcao(entrada(f"Frequência {FREQUENCIAS_VALIDAS}: "), FREQUENCIAS_VALIDAS, "frequência")
            data_str = entrada("Próxima execução (AAAA-MM-DD): ")
            novo_id = repo.criar(
                CalendarioPreventivo(
                    maquina_id=maquina_id,
                    titulo=titulo,
                    frequencia=frequencia,
                    data_proxima_execucao=datetime.strptime(data_str, "%Y-%m-%d").date(),
                )
            )
            print(f"Agendamento criado com id {novo_id}.")
        elif opcao == "2":
            inicio = datetime.strptime(entrada("Data início (AAAA-MM-DD): "), "%Y-%m-%d").date()
            fim = datetime.strptime(entrada("Data fim (AAAA-MM-DD): "), "%Y-%m-%d").date()
            for c in repo.listar_por_periodo(inicio, fim):
                print(f"{c.id} | {c.titulo} | máquina={c.maquina_id} | {c.data_proxima_execucao} | {c.status}")
        elif opcao == "3":
            id_ = int(entrada("ID do agendamento: "))
            atualizado = repo.marcar_concluida(id_)
            print(f"Concluído. Próxima ocorrência já agendada (id original {atualizado.id}).")
        elif opcao == "4":
            repo.marcar_atrasadas()
            for c in repo.listar_atrasadas():
                print(f"{c.id} | {c.titulo} | máquina={c.maquina_id} | venceu em {c.data_proxima_execucao}")
        elif opcao == "0":
            return


# --------------------------------------------------------------------------
# Menu principal
# --------------------------------------------------------------------------

def menu_principal():
    while True:
        print(f"\n=== PORTAL DA MANUTENÇÃO — {usuario_logado.nome} ({perfil_logado}) ===")
        print("1) Administração (perfis/turmas/usuários)")
        print("2) Mapa da Oficina (setores/máquinas)")
        print("3) Almoxarifado/Ferramentaria")
        print("4) Alertas de Estoque")
        print("5) Registro de Quebra de Ferramenta/Item")
        print("6) Solicitação de Serviço (SS) / Ordem de Serviço (OS)")
        print("7) Solicitação de Compras")
        print("8) Calendário Preventivo")
        print("0) Sair")
        opcao = entrada("Opção: ")

        try:
            if opcao == "1":
                menu_administracao()
            elif opcao == "2":
                menu_mapa_oficina()
            elif opcao == "3":
                menu_almoxarifado()
            elif opcao == "4":
                menu_alertas_estoque()
            elif opcao == "5":
                menu_registro_quebra()
            elif opcao == "6":
                menu_ss_os()
            elif opcao == "7":
                menu_compras()
            elif opcao == "8":
                menu_calendario_preventivo()
            elif opcao == "0":
                print("Até logo!")
                return
            else:
                print("Opção inválida.")
        except PermissionError as erro:
            print(f"Acesso negado: {erro}")
        except ValidacaoError as erro:
            print(f"Erro de validação: {erro}")


def menu_administracao():
    exige_perfil(perfil_logado, ("coordenador", "gestor", "professor"))
    while True:
        print("\n--- Administração --- (1) Perfis (2) Turmas (3) Usuários (0) Voltar")
        opcao = entrada("Opção: ")
        if opcao == "1":
            menu_crud_perfis()
        elif opcao == "2":
            menu_crud_turmas()
        elif opcao == "3":
            menu_crud_usuarios()
        elif opcao == "0":
            return


def menu_mapa_oficina():
    while True:
        print("\n--- Mapa da Oficina --- (1) Setores (2) Máquinas (0) Voltar")
        opcao = entrada("Opção: ")
        if opcao == "1":
            menu_crud_setores()
        elif opcao == "2":
            menu_crud_maquinas()
        elif opcao == "0":
            return
