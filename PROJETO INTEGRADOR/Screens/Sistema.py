import flet as ft
import sqlite3
from Dados.Conexao import (
    inicializar_banco, salvar_computador, buscar_computadores,
    atualizar_computador, excluir_computador,
    salvar_chamado, buscar_chamados, atualizar_status_chamado,
    excluir_chamado, dados_para_chamado, salvar_solucao,
    salvar_tecnico, buscar_tecnicos, atualizar_tecnico, excluir_tecnico,
    quantidade_computadores, quantidade_tecnicos,
    chamados_abertos, chamados_atendimento, chamados_resolvidos
)


# ==========================================================
# CORES DO SISTEMA - AZUL + ROXO AZULADO
# ==========================================================

FUNDO = "#F4F5FA"

LATERAL = "#1565C0"

CARD = "#FFFFFF"

AZUL = "#1976D2"
AZUL_ESCURO = "#0D47A1"

ROXO = "#4B4E9E"
ROXO_CLARO = "#E8E8F3"

TEXTO = "#1F2937"
TEXTO_SECUNDARIO = "#64748B"

BRANCO = "#FFFFFF"

VERDE = "#16A34A"
VERMELHO = "#DC2626"


def sistema(page: ft.Page, usuario_logado=None):

    inicializar_banco()

    page.title = "TECHHELP"
    page.bgcolor = FUNDO
    page.padding = 0
    page.window.maximized = True

    conteudo = ft.Column(
        expand=True,
        spacing=15,
        scroll=ft.ScrollMode.AUTO
    )

    # ==========================================================
    # AVISOS
    # ==========================================================

    def aviso(texto, erro=False):

        page.snack_bar = ft.SnackBar(
            ft.Text(
                texto,
                color=BRANCO
            ),
            bgcolor=VERMELHO if erro else VERDE
        )

        page.snack_bar.open = True
        page.update()

    # ==========================================================
    # CAMPOS
    # ==========================================================

    def campo(label, width=220):

        return ft.TextField(
            label=label,
            width=width,
            bgcolor=BRANCO,
            color=TEXTO,
            border_color="#D8D9E5",
            focused_border_color=ROXO,
            label_style=ft.TextStyle(
                color=TEXTO_SECUNDARIO
            )
        )

    # ==========================================================
    # CARDS DO DASHBOARD
    # ==========================================================

    def card(numero, texto):

        return ft.Container(
            width=190,
            height=120,
            bgcolor=CARD,
            border_radius=15,
            padding=18,

            border=ft.Border.all(
                1,
                "#E2E4ED"
            ),

            content=ft.Column([

                ft.Text(
                    str(numero).zfill(2),
                    size=30,
                    weight=ft.FontWeight.BOLD,
                    color=ROXO
                ),

                ft.Text(
                    texto,
                    color=TEXTO
                )
            ])
        )

    # ==========================================================
    # DASHBOARD
    # ==========================================================

    def dashboard():

        conteudo.controls.clear()

        conteudo.controls.extend([

            ft.Text(
                "INÍCIO",
                size=30,
                weight=ft.FontWeight.BOLD,
                color=TEXTO
            ),

            ft.Text(
                f"Bem-vindo, "
                f"{usuario_logado[1] if usuario_logado else 'usuário'}",
                color=TEXTO_SECUNDARIO
            ),

            ft.Row(
                [
                    card(
                        quantidade_computadores(),
                        "Computadores"
                    ),

                    card(
                        chamados_abertos(),
                        "Chamados Abertos"
                    ),

                    card(
                        chamados_atendimento(),
                        "Em Atendimento"
                    ),

                    card(
                        chamados_resolvidos(),
                        "Resolvidos"
                    ),

                    card(
                        quantidade_tecnicos(),
                        "Técnicos"
                    )
                ],

                wrap=True,
                spacing=12
            ),

            ft.Container(
                bgcolor=CARD,
                border_radius=15,
                padding=20,

                border=ft.Border.all(
                    1,
                    "#E2E4ED"
                ),

                content=ft.Column([

                    ft.Text(
                        "Status do sistema",
                        size=20,
                        weight=ft.FontWeight.BOLD,
                        color=TEXTO
                    ),

                    ft.Text(
                        "Banco de dados conectado e atualizado "
                        "em tempo real.",
                        color=TEXTO_SECUNDARIO
                    )
                ])
            )
        ])

        page.update()

    # ==========================================================
    # COMPUTADORES
    # ==========================================================

    def computadores():

        conteudo.controls.clear()

        id_edicao = {
            "valor": None
        }

        patrimonio = campo("Patrimônio")
        modelo = campo("Modelo")
        laboratorio = campo("Laboratório")
        sistema_op = campo("Sistema Operacional")

        status = ft.Dropdown(
            label="Status",
            width=220,
            bgcolor=BRANCO,
            color=TEXTO,
            filled=True,
            fill_color=BRANCO,
            border_color="#D8D9E5",

            options=[
                ft.dropdown.Option("Ativo"),
                ft.dropdown.Option("Manutenção"),
                ft.dropdown.Option("Inativo")
            ]
        )

        tabela = ft.DataTable(

            columns=[

                ft.DataColumn(
                    ft.Text("ID", color=TEXTO)
                ),

                ft.DataColumn(
                    ft.Text("Patrimônio", color=TEXTO)
                ),

                ft.DataColumn(
                    ft.Text("Modelo", color=TEXTO)
                ),

                ft.DataColumn(
                    ft.Text("Laboratório", color=TEXTO)
                ),

                ft.DataColumn(
                    ft.Text("Sistema", color=TEXTO)
                ),

                ft.DataColumn(
                    ft.Text("Status", color=TEXTO)
                ),

                ft.DataColumn(
                    ft.Text("Ações", color=TEXTO)
                )
            ],

            rows=[],

            border=ft.Border.all(
                1,
                "#D8D9E5"
            ),

            horizontal_lines=ft.BorderSide(
                1,
                "#E8E9F0"
            ),

            vertical_lines=ft.BorderSide(
                1,
                "#E8E9F0"
            )
        )

        def limpar():

            id_edicao["valor"] = None

            patrimonio.value = ""
            modelo.value = ""
            laboratorio.value = ""
            sistema_op.value = ""
            status.value = None

        def carregar():

            tabela.rows.clear()

            for item in buscar_computadores():

                tabela.rows.append(

                    ft.DataRow(

                        cells=[

                            ft.DataCell(
                                ft.Text(
                                    str(item[0]),
                                    color=TEXTO
                                )
                            ),

                            ft.DataCell(
                                ft.Text(
                                    str(item[1]),
                                    color=TEXTO
                                )
                            ),

                            ft.DataCell(
                                ft.Text(
                                    str(item[2]),
                                    color=TEXTO
                                )
                            ),

                            ft.DataCell(
                                ft.Text(
                                    str(item[3]),
                                    color=TEXTO
                                )
                            ),

                            ft.DataCell(
                                ft.Text(
                                    str(item[4]),
                                    color=TEXTO
                                )
                            ),

                            ft.DataCell(
                                ft.Text(
                                    str(item[5]),
                                    color=TEXTO
                                )
                            ),

                            ft.DataCell(

                                ft.Row([

                                    ft.IconButton(
                                        ft.Icons.EDIT,
                                        icon_color=ROXO,
                                        on_click=lambda e, x=item:
                                        editar(x)
                                    ),

                                    ft.IconButton(
                                        ft.Icons.DELETE,
                                        icon_color=VERMELHO,
                                        on_click=lambda e, x=item:
                                        apagar(x[0])
                                    )
                                ])
                            )
                        ]
                    )
                )

        def editar(item):

            id_edicao["valor"] = item[0]

            patrimonio.value = item[1]
            modelo.value = item[2]
            laboratorio.value = item[3]
            sistema_op.value = item[4]
            status.value = item[5]

            btn.text = "Salvar alteração"

            page.update()

        def apagar(id_):

            try:

                excluir_computador(id_)

                carregar()

                aviso(
                    "Computador excluído."
                )

            except Exception as erro:

                aviso(
                    f"Não foi possível excluir: {erro}",
                    True
                )

        def salvar(e):

            if (
                not patrimonio.value
                or not modelo.value
                or not laboratorio.value
                or not sistema_op.value
            ):

                aviso(
                    "Preencha todos os campos do computador.",
                    True
                )

                return

            try:

                if id_edicao["valor"] is None:

                    salvar_computador(
                        patrimonio.value,
                        modelo.value,
                        laboratorio.value,
                        sistema_op.value,
                        status.value or "Ativo"
                    )

                    aviso(
                        "Computador cadastrado."
                    )

                else:

                    atualizar_computador(
                        id_edicao["valor"],
                        patrimonio.value,
                        modelo.value,
                        laboratorio.value,
                        sistema_op.value,
                        status.value or "Ativo"
                    )

                    aviso(
                        "Computador atualizado."
                    )

                limpar()

                btn.text = "Cadastrar computador"

                carregar()

                page.update()

            except Exception as erro:

                aviso(
                    f"Erro: {erro}",
                    True
                )

        btn = ft.ElevatedButton(
            "Cadastrar computador",
            icon=ft.Icons.ADD,
            on_click=salvar,
            bgcolor=ROXO,
            color=BRANCO
        )

        conteudo.controls.extend([

            ft.Text(
                "COMPUTADORES",
                size=30,
                weight=ft.FontWeight.BOLD,
                color=TEXTO
            ),

            ft.Row(
                [
                    patrimonio,
                    modelo,
                    laboratorio
                ],
                wrap=True
            ),

            ft.Row(
                [
                    sistema_op,
                    status,
                    btn
                ],
                wrap=True
            ),

            ft.Container(
                bgcolor=CARD,
                border_radius=15,
                padding=15,

                content=ft.Row(
                    [tabela],
                    scroll=ft.ScrollMode.AUTO
                ),

                expand=True
            )
        ])

        carregar()

        page.update()

    # ==========================================================
    # CHAMADOS
    # ==========================================================

    def chamados():

        conteudo.controls.clear()

        computadores_db, usuarios_db = dados_para_chamado()

        if not computadores_db:

            conteudo.controls.extend([

                ft.Text(
                    "CHAMADOS",
                    size=30,
                    weight=ft.FontWeight.BOLD,
                    color=TEXTO
                ),

                ft.Text(
                    "Cadastre pelo menos um computador antes "
                    "de abrir um chamado.",
                    color=TEXTO_SECUNDARIO
                )
            ])

            page.update()

            return

        computador = ft.Dropdown(
            label="Computador",
            width=300,
            bgcolor=BRANCO,
            color=TEXTO,
            filled=True,
            fill_color=BRANCO,
            border_color="#D8D9E5",

            options=[

                ft.dropdown.Option(
                    str(x[0]),
                    f"{x[1]} - {x[2]}"
                )

                for x in computadores_db
            ]
        )

        usuario = ft.Dropdown(
            label="Usuário",
            width=250,
            bgcolor=BRANCO,
            color=TEXTO,
            filled=True,
            fill_color=BRANCO,
            border_color="#D8D9E5",

            options=[

                ft.dropdown.Option(
                    str(x[0]),
                    x[1]
                )

                for x in usuarios_db
            ]
        )

        prioridade = ft.Dropdown(
            label="Prioridade",
            width=180,
            bgcolor=BRANCO,
            color=TEXTO,
            filled=True,
            fill_color=BRANCO,
            border_color="#D8D9E5",

            options=[
                ft.dropdown.Option("Baixa"),
                ft.dropdown.Option("Média"),
                ft.dropdown.Option("Alta"),
                ft.dropdown.Option("Urgente")
            ]
        )

        descricao = ft.TextField(
            label="Descrição do problema",
            multiline=True,
            width=500,
            height=80,
            bgcolor=BRANCO,
            color=TEXTO,
            border_color="#D8D9E5",
            focused_border_color=ROXO
        )

        tabela = ft.DataTable(

            columns=[

                ft.DataColumn(
                    ft.Text(
                        x,
                        color=TEXTO
                    )
                )

                for x in [
                    "ID",
                    "PC",
                    "Patrimônio",
                    "Usuário",
                    "Descrição",
                    "Prioridade",
                    "Status",
                    "Data",
                    "Ações"
                ]
            ],

            rows=[],

            border=ft.Border.all(
                1,
                "#D8D9E5"
            ),

            horizontal_lines=ft.BorderSide(
                1,
                "#E8E9F0"
            ),

            vertical_lines=ft.BorderSide(
                1,
                "#E8E9F0"
            )
        )

        def carregar():

            tabela.rows.clear()

            for item in buscar_chamados():

                tabela.rows.append(

                    ft.DataRow(

                        cells=[

                            ft.DataCell(
                                ft.Text(
                                    str(item[0]),
                                    color=TEXTO
                                )
                            ),

                            ft.DataCell(
                                ft.Text(
                                    str(item[1]),
                                    color=TEXTO
                                )
                            ),

                            ft.DataCell(
                                ft.Text(
                                    str(item[2]),
                                    color=TEXTO
                                )
                            ),

                            ft.DataCell(
                                ft.Text(
                                    str(item[3]),
                                    color=TEXTO
                                )
                            ),

                            ft.DataCell(
                                ft.Text(
                                    str(item[4]),
                                    color=TEXTO
                                )
                            ),

                            ft.DataCell(
                                ft.Text(
                                    str(item[5]),
                                    color=TEXTO
                                )
                            ),

                            ft.DataCell(
                                ft.Text(
                                    str(item[6]),
                                    color=TEXTO
                                )
                            ),

                            ft.DataCell(
                                ft.Text(
                                    str(item[7]),
                                    color=TEXTO
                                )
                            ),

                            ft.DataCell(

                                ft.Row([

                                    ft.IconButton(
                                        ft.Icons.PLAY_ARROW,
                                        tooltip="Em atendimento",
                                        icon_color=AZUL,

                                        on_click=lambda e,
                                        id_=item[0]:
                                        mudar_status(
                                            id_,
                                            "Em Atendimento"
                                        )
                                    ),

                                    ft.IconButton(
                                        ft.Icons.CHECK,
                                        tooltip="Resolver",
                                        icon_color=VERDE,

                                        on_click=lambda e,
                                        id_=item[0]:
                                        resolver(id_)
                                    ),

                                    ft.IconButton(
                                        ft.Icons.DELETE,
                                        tooltip="Excluir",
                                        icon_color=VERMELHO,

                                        on_click=lambda e,
                                        id_=item[0]:
                                        apagar(id_)
                                    )
                                ])
                            )
                        ]
                    )
                )

        def cadastrar(e):

            if (
                not computador.value
                or not descricao.value
                or not prioridade.value
            ):

                aviso(
                    "Preencha computador, descrição e prioridade.",
                    True
                )

                return

            try:

                salvar_chamado(
                    int(computador.value),

                    int(usuario.value)
                    if usuario.value
                    else None,

                    descricao.value,
                    prioridade.value
                )

                descricao.value = ""
                prioridade.value = None
                computador.value = None
                usuario.value = None

                carregar()

                aviso(
                    "Chamado cadastrado."
                )

                page.update()

            except Exception as erro:

                aviso(
                    f"Erro ao cadastrar chamado: {erro}",
                    True
                )

        def mudar_status(id_, novo_status):

            try:

                atualizar_status_chamado(
                    id_,
                    novo_status
                )

                carregar()

                aviso(
                    f"Chamado atualizado para: {novo_status}"
                )

            except Exception as erro:

                aviso(
                    f"Erro: {erro}",
                    True
                )

        def resolver(id_):

            tecnicos_db = buscar_tecnicos()

            if not tecnicos_db:

                aviso(
                    "Cadastre um técnico antes de resolver chamados.",
                    True
                )

                return

            tecnico = ft.Dropdown(
                label="Técnico",
                width=300,
                bgcolor=BRANCO,
                color=TEXTO,
                border_color="#D8D9E5",

                options=[

                    ft.dropdown.Option(
                        str(x[0]),
                        x[1]
                    )

                    for x in tecnicos_db
                ]
            )

            solucao = ft.TextField(
                label="Solução aplicada",
                multiline=True,
                width=500,
                bgcolor=BRANCO,
                color=TEXTO,
                border_color="#D8D9E5",
                focused_border_color=ROXO
            )

            def fechar(e=None):

                dlg.open = False

                page.update()

            def confirmar(e):

                if (
                    not tecnico.value
                    or not solucao.value.strip()
                ):

                    aviso(
                        "Informe o técnico e a solução.",
                        True
                    )

                    return

                try:

                    salvar_solucao(
                        id_,
                        int(tecnico.value),
                        solucao.value
                    )

                    dlg.open = False

                    page.update()

                    carregar()

                    aviso(
                        "Chamado resolvido e solução registrada."
                    )

                except Exception as erro:

                    aviso(
                        f"Erro: {erro}",
                        True
                    )

            dlg = ft.AlertDialog(

                modal=True,

                title=ft.Text(
                    "Resolver chamado",
                    color=TEXTO
                ),

                content=ft.Column(
                    [
                        tecnico,
                        solucao
                    ],
                    tight=True
                ),

                actions=[

                    ft.TextButton(
                        "Cancelar",
                        on_click=fechar
                    ),

                    ft.ElevatedButton(
                        "Resolver",
                        on_click=confirmar,
                        bgcolor=ROXO,
                        color=BRANCO
                    )
                ]
            )

            page.overlay.append(dlg)

            dlg.open = True

            page.update()

        def apagar(id_):

            try:

                excluir_chamado(id_)

                carregar()

                aviso(
                    "Chamado excluído."
                )

            except Exception as erro:

                aviso(
                    f"Erro: {erro}",
                    True
                )

        conteudo.controls.extend([

            ft.Text(
                "CHAMADOS",
                size=30,
                weight=ft.FontWeight.BOLD,
                color=TEXTO
            ),

            ft.Row(
                [
                    computador,
                    usuario,
                    prioridade
                ],
                wrap=True
            ),

            descricao,

            ft.ElevatedButton(
                "Cadastrar chamado",
                icon=ft.Icons.ADD,
                on_click=cadastrar,
                bgcolor=ROXO,
                color=BRANCO
            ),

            ft.Container(
                bgcolor=CARD,
                border_radius=15,
                padding=15,

                content=ft.Row(
                    [tabela],
                    scroll=ft.ScrollMode.AUTO
                ),

                expand=True
            )
        ])

        carregar()

        page.update()

    # ==========================================================
    # TÉCNICOS
    # ==========================================================

    def tecnicos():

        conteudo.controls.clear()

        id_edicao = {
            "valor": None
        }

        nome = campo(
            "Nome",
            210
        )

        email = campo(
            "E-mail",
            240
        )

        telefone = campo(
            "Telefone",
            170
        )

        especialidade = campo(
            "Especialidade",
            210
        )

        status = ft.Dropdown(
            label="Status",
            width=160,
            bgcolor=BRANCO,
            color=TEXTO,
            filled=True,
            fill_color=BRANCO,
            border_color="#D8D9E5",

            options=[
                ft.dropdown.Option("Ativo"),
                ft.dropdown.Option("Inativo"),
                ft.dropdown.Option("Férias")
            ]
        )

        tabela = ft.DataTable(

            columns=[

                ft.DataColumn(
                    ft.Text(
                        x,
                        color=TEXTO
                    )
                )

                for x in [
                    "ID",
                    "Nome",
                    "E-mail",
                    "Telefone",
                    "Especialidade",
                    "Status",
                    "Ações"
                ]
            ],

            rows=[],

            border=ft.Border.all(
                1,
                "#D8D9E5"
            ),

            horizontal_lines=ft.BorderSide(
                1,
                "#E8E9F0"
            ),

            vertical_lines=ft.BorderSide(
                1,
                "#E8E9F0"
            )
        )

        def limpar():

            id_edicao["valor"] = None

            nome.value = ""
            email.value = ""
            telefone.value = ""
            especialidade.value = ""
            status.value = None

        def carregar():

            tabela.rows.clear()

            for item in buscar_tecnicos():

                tabela.rows.append(

                    ft.DataRow(

                        cells=[

                            ft.DataCell(
                                ft.Text(
                                    str(item[0]),
                                    color=TEXTO
                                )
                            ),

                            ft.DataCell(
                                ft.Text(
                                    str(item[1]),
                                    color=TEXTO
                                )
                            ),

                            ft.DataCell(
                                ft.Text(
                                    str(item[2]),
                                    color=TEXTO
                                )
                            ),

                            ft.DataCell(
                                ft.Text(
                                    str(item[3] or ""),
                                    color=TEXTO
                                )
                            ),

                            ft.DataCell(
                                ft.Text(
                                    str(item[4] or ""),
                                    color=TEXTO
                                )
                            ),

                            ft.DataCell(
                                ft.Text(
                                    str(item[5]),
                                    color=TEXTO
                                )
                            ),

                            ft.DataCell(

                                ft.Row([

                                    ft.IconButton(
                                        ft.Icons.EDIT,
                                        icon_color=ROXO,

                                        on_click=lambda e, x=item:
                                        editar(x)
                                    ),

                                    ft.IconButton(
                                        ft.Icons.DELETE,
                                        icon_color=VERMELHO,

                                        on_click=lambda e,
                                        id_=item[0]:
                                        apagar(id_)
                                    )
                                ])
                            )
                        ]
                    )
                )

        def editar(item):

            id_edicao["valor"] = item[0]

            nome.value = item[1]
            email.value = item[2]
            telefone.value = item[3] or ""
            especialidade.value = item[4] or ""
            status.value = item[5]

            btn.text = "Salvar alteração"

            page.update()

        def apagar(id_):

            try:

                excluir_tecnico(id_)

                carregar()

                aviso(
                    "Técnico excluído."
                )

            except Exception:

                aviso(
                    "Não é possível excluir este técnico porque "
                    "ele possui soluções vinculadas a chamados.",
                    True
                )

        def salvar(e):

            if (
                not nome.value.strip()
                or not email.value.strip()
            ):

                aviso(
                    "Nome e e-mail são obrigatórios.",
                    True
                )

                return

            try:

                if id_edicao["valor"] is None:

                    salvar_tecnico(
                        nome.value,
                        email.value,
                        telefone.value,
                        especialidade.value,
                        status.value or "Ativo"
                    )

                    aviso(
                        "Técnico cadastrado."
                    )

                else:

                    atualizar_tecnico(
                        id_edicao["valor"],
                        nome.value,
                        email.value,
                        telefone.value,
                        especialidade.value,
                        status.value or "Ativo"
                    )

                    aviso(
                        "Técnico atualizado."
                    )

                limpar()

                btn.text = "Cadastrar técnico"

                carregar()

                page.update()

            except Exception as erro:

                aviso(
                    f"Erro: {erro}",
                    True
                )

        btn = ft.ElevatedButton(
            "Cadastrar técnico",
            icon=ft.Icons.ADD,
            on_click=salvar,
            bgcolor=ROXO,
            color=BRANCO
        )

        conteudo.controls.extend([

            ft.Text(
                "TÉCNICOS",
                size=30,
                weight=ft.FontWeight.BOLD,
                color=TEXTO
            ),

            ft.Text(
                "Cadastro e gerenciamento dos técnicos.",
                color=TEXTO_SECUNDARIO
            ),

            ft.Row(
                [
                    nome,
                    email,
                    telefone
                ],
                wrap=True
            ),

            ft.Row(
                [
                    especialidade,
                    status,
                    btn
                ],
                wrap=True
            ),

            ft.Container(
                bgcolor=CARD,
                border_radius=15,
                padding=15,

                content=ft.Row(
                    [tabela],
                    scroll=ft.ScrollMode.AUTO
                ),

                expand=True
            )
        ])

        carregar()

        page.update()

    # ==========================================================
    # ESTOQUE
    # ==========================================================

    def banco_local():
        conexao = sqlite3.connect("Dados/banco.db")
        conexao.execute("PRAGMA foreign_keys = ON")
        return conexao

    def preparar_estoque():
        conexao = banco_local()
        conexao.execute("""
            CREATE TABLE IF NOT EXISTS ESTOQUE (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                peca TEXT NOT NULL,
                quantidade INTEGER NOT NULL DEFAULT 1,
                estado TEXT NOT NULL,
                observacao TEXT
            )
        """)
        conexao.commit()
        conexao.close()

    def estoque():
        preparar_estoque()
        conteudo.controls.clear()

        id_edicao = {"valor": None}

        peca = campo("Peça", 240)
        quantidade = campo("Quantidade", 130)
        estado = ft.Dropdown(
            label="Estado",
            width=180,
            bgcolor=BRANCO,
            color=TEXTO,
            filled=True,
            fill_color=BRANCO,
            border_color="#D8D9E5",
            options=[
                ft.dropdown.Option("Boa"),
                ft.dropdown.Option("Usada"),
                ft.dropdown.Option("Para reutilização"),
                ft.dropdown.Option("Com defeito")
            ]
        )
        observacao = campo("Observação", 300)

        tabela = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text(x, color=TEXTO))
                for x in ["ID", "Peça", "Quantidade", "Estado", "Observação", "Ações"]
            ],
            rows=[],
            border=ft.Border.all(1, "#D8D9E5"),
            horizontal_lines=ft.BorderSide(1, "#E8E9F0"),
            vertical_lines=ft.BorderSide(1, "#E8E9F0")
        )

        def limpar():
            id_edicao["valor"] = None
            peca.value = ""
            quantidade.value = ""
            estado.value = None
            observacao.value = ""

        def carregar():
            tabela.rows.clear()
            conexao = banco_local()
            dados = conexao.execute(
                "SELECT id, peca, quantidade, estado, observacao "
                "FROM ESTOQUE ORDER BY id DESC"
            ).fetchall()
            conexao.close()

            for item in dados:
                tabela.rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(str(item[0]), color=TEXTO)),
                            ft.DataCell(ft.Text(str(item[1]), color=TEXTO)),
                            ft.DataCell(ft.Text(str(item[2]), color=TEXTO)),
                            ft.DataCell(ft.Text(str(item[3]), color=TEXTO)),
                            ft.DataCell(ft.Text(str(item[4] or ""), color=TEXTO)),
                            ft.DataCell(
                                ft.Row([
                                    ft.IconButton(
                                        ft.Icons.EDIT,
                                        icon_color=ROXO,
                                        on_click=lambda e, x=item: editar(x)
                                    ),
                                    ft.IconButton(
                                        ft.Icons.DELETE,
                                        icon_color=VERMELHO,
                                        on_click=lambda e, id_=item[0]: apagar(id_)
                                    )
                                ])
                            )
                        ]
                    )
                )

        def editar(item):
            id_edicao["valor"] = item[0]
            peca.value = item[1]
            quantidade.value = str(item[2])
            estado.value = item[3]
            observacao.value = item[4] or ""
            btn.text = "Salvar alteração"
            page.update()

        def apagar(id_):
            try:
                conexao = banco_local()
                conexao.execute("DELETE FROM ESTOQUE WHERE id = ?", (id_,))
                conexao.commit()
                conexao.close()
                carregar()
                aviso("Item removido do estoque.")
                page.update()
            except Exception as erro:
                aviso(f"Erro: {erro}", True)

        def salvar(e):
            if not peca.value.strip() or not quantidade.value.strip() or not estado.value:
                aviso("Preencha peça, quantidade e estado.", True)
                return

            try:
                quantidade_int = int(quantidade.value)
                if quantidade_int < 1:
                    raise ValueError

                conexao = banco_local()

                if id_edicao["valor"] is None:
                    conexao.execute(
                        "INSERT INTO ESTOQUE (peca, quantidade, estado, observacao) "
                        "VALUES (?, ?, ?, ?)",
                        (peca.value, quantidade_int, estado.value, observacao.value)
                    )
                    mensagem = "Item adicionado ao estoque."
                else:
                    conexao.execute(
                        "UPDATE ESTOQUE SET peca = ?, quantidade = ?, estado = ?, "
                        "observacao = ? WHERE id = ?",
                        (
                            peca.value,
                            quantidade_int,
                            estado.value,
                            observacao.value,
                            id_edicao["valor"]
                        )
                    )
                    mensagem = "Item do estoque atualizado."

                conexao.commit()
                conexao.close()

                limpar()
                btn.text = "Adicionar ao estoque"
                carregar()
                aviso(mensagem)
                page.update()

            except ValueError:
                aviso("A quantidade deve ser um número inteiro maior que zero.", True)
            except Exception as erro:
                aviso(f"Erro: {erro}", True)

        btn = ft.ElevatedButton(
            "Adicionar ao estoque",
            icon=ft.Icons.ADD,
            on_click=salvar,
            bgcolor=ROXO,
            color=BRANCO
        )

        conteudo.controls.extend([
            ft.Text(
                "ESTOQUE",
                size=30,
                weight=ft.FontWeight.BOLD,
                color=TEXTO
            ),
            ft.Text(
                "Controle de peças disponíveis, sobras e itens que podem ser reutilizados.",
                color=TEXTO_SECUNDARIO
            ),
            ft.Row(
                [peca, quantidade, estado, observacao],
                wrap=True
            ),
            btn,
            ft.Container(
                bgcolor=CARD,
                border_radius=15,
                padding=15,
                content=ft.Row(
                    [tabela],
                    scroll=ft.ScrollMode.AUTO
                ),
                expand=True
            )
        ])

        carregar()
        page.update()

    # ==========================================================
    # HISTÓRICO
    # ==========================================================

    def historico():
        conteudo.controls.clear()

        tabela = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text(x, color=TEXTO))
                for x in [
                    "Chamado",
                    "Técnico",
                    "Computador",
                    "Patrimônio",
                    "Descrição",
                    "Solução",
                    "Data"
                ]
            ],
            rows=[],
            border=ft.Border.all(1, "#D8D9E5"),
            horizontal_lines=ft.BorderSide(1, "#E8E9F0"),
            vertical_lines=ft.BorderSide(1, "#E8E9F0")
        )

        ranking = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Técnico", color=TEXTO)),
                ft.DataColumn(ft.Text("Atendimentos", color=TEXTO))
            ],
            rows=[],
            border=ft.Border.all(1, "#D8D9E5"),
            horizontal_lines=ft.BorderSide(1, "#E8E9F0"),
            vertical_lines=ft.BorderSide(1, "#E8E9F0")
        )

        def carregar():
            tabela.rows.clear()
            ranking.rows.clear()

            conexao = banco_local()

            atendimentos = conexao.execute("""
                SELECT
                    a.id_chamado,
                    t.nome,
                    c.modelo,
                    c.patrimonio,
                    ch.descricao,
                    a.descricao,
                    a.data_atendimento
                FROM ATENDIMENTO a
                INNER JOIN TECNICOS t ON t.id = a.id_tecnico
                INNER JOIN CHAMADOS ch ON ch.id = a.id_chamado
                INNER JOIN COMPUTADORES c ON c.id = ch.computador_id
                ORDER BY a.data_atendimento DESC
            """).fetchall()

            tecnicos = conexao.execute("""
                SELECT
                    t.nome,
                    COUNT(a.id) AS total
                FROM TECNICOS t
                LEFT JOIN ATENDIMENTO a ON a.id_tecnico = t.id
                GROUP BY t.id, t.nome
                ORDER BY total DESC, t.nome
            """).fetchall()

            conexao.close()

            for item in atendimentos:
                tabela.rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(str(item[0]), color=TEXTO)),
                            ft.DataCell(ft.Text(str(item[1]), color=TEXTO)),
                            ft.DataCell(ft.Text(str(item[2]), color=TEXTO)),
                            ft.DataCell(ft.Text(str(item[3]), color=TEXTO)),
                            ft.DataCell(ft.Text(str(item[4]), color=TEXTO)),
                            ft.DataCell(ft.Text(str(item[5]), color=TEXTO)),
                            ft.DataCell(ft.Text(str(item[6]), color=TEXTO))
                        ]
                    )
                )

            for item in tecnicos:
                ranking.rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(str(item[0]), color=TEXTO)),
                            ft.DataCell(ft.Text(str(item[1]), color=TEXTO))
                        ]
                    )
                )

        conteudo.controls.extend([
            ft.Text(
                "HISTÓRICO",
                size=30,
                weight=ft.FontWeight.BOLD,
                color=TEXTO
            ),
            ft.Text(
                "Acompanhe os atendimentos realizados e o desempenho dos técnicos.",
                color=TEXTO_SECUNDARIO
            ),
            ft.Container(
                bgcolor=CARD,
                border_radius=15,
                padding=20,
                border=ft.Border.all(1, "#E2E4ED"),
                content=ft.Column([
                    ft.Text(
                        "Técnicos com mais atendimentos",
                        size=20,
                        weight=ft.FontWeight.BOLD,
                        color=TEXTO
                    ),
                    ft.Row(
                        [ranking],
                        scroll=ft.ScrollMode.AUTO
                    )
                ])
            ),
            ft.Container(
                bgcolor=CARD,
                border_radius=15,
                padding=15,
                content=ft.Row(
                    [tabela],
                    scroll=ft.ScrollMode.AUTO
                ),
                expand=True
            )
        ])

        carregar()
        page.update()

    # ==========================================================
    # LOGOUT
    # ==========================================================

    def logout(e=None):

        from Screens.Login import Login

        page.clean()

        Login(page)

    # ==========================================================
    # BOTÕES DO MENU
    # ==========================================================

    def menu_botao(texto, icone, funcao):

        return ft.Container(

            width=170,
            height=45,

            bgcolor="#1565C0",

            border=ft.Border.all(
                1,
                "BLACK"
            ),

            border_radius=25,

            content=ft.TextButton(

                texto,

                icon=icone,

                style=ft.ButtonStyle(
                    color="BLACK"
                ),

                on_click=lambda e: funcao()
            )
        )

    # ==========================================================
    # MENU LATERAL
    # ==========================================================

    lateral = ft.Container(

        width=240,

        bgcolor=LATERAL,

        padding=30,

        content=ft.Column(

            [

                # LOGO MENOR
                ft.Container(

                    width=180,
                    height=145,

                    alignment=ft.Alignment.CENTER,
                    

                    content=ft.Image(
                        src="image.png",
                        width=180,
                        height=180
                    )
                ),

                ft.Divider(
                    color="BLACK"
                ),

                ft.Container(
                    expand=True,
                    content=ft.Column(
                        [
                            menu_botao(
                                "Início",
                                ft.Icons.HOME,
                                dashboard
                            ),
                            menu_botao(
                                "PCs",
                                ft.Icons.COMPUTER,
                                computadores
                            ),
                            menu_botao(
                                "Chamados",
                                ft.Icons.WARNING,
                                chamados
                            ),
                            menu_botao(
                                "Técnicos",
                                ft.Icons.PERSON,
                                tecnicos
                            ),
                            menu_botao(
                                "Estoque",
                                ft.Icons.INVENTORY_2,
                                estoque
                            ),
                            menu_botao(
                                "Histórico",
                                ft.Icons.HISTORY,
                                historico
                            )
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=18
                    )
                ),

                menu_botao(
                    "Logout",
                    ft.Icons.LOGOUT,
                    logout
                )
            ],

            spacing=18,
            expand=True
        )
    )

    # ==========================================================
    # LAYOUT PRINCIPAL
    # ==========================================================

    page.add(

        ft.Row(

            [

                lateral,

                ft.Container(
                    expand=True,
                    padding=35,
                    content=conteudo
                )
            ],

            expand=True,
            spacing=0
        )
    )

    dashboard()
