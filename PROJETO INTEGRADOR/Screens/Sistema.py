import flet as ft
from Dados.Conexao import (
    inicializar_banco, salvar_computador, buscar_computadores,
    atualizar_computador, excluir_computador,
    salvar_chamado, buscar_chamados, atualizar_status_chamado,
    excluir_chamado, dados_para_chamado, salvar_solucao,
    salvar_tecnico, buscar_tecnicos, atualizar_tecnico, excluir_tecnico,
    quantidade_computadores, quantidade_tecnicos,
    chamados_abertos, chamados_atendimento, chamados_resolvidos
)

FUNDO = "#1E1B2E"
LATERAL = "#2B2845"
CARD = "#302C4A"
VERDE = "#00F080"
BRANCO = "#F5F5F5"


def sistema(page: ft.Page, usuario_logado=None):
    inicializar_banco()
    page.title = "TECHHELP"
    page.bgcolor = FUNDO
    page.padding = 0
    page.window.maximized = True

    conteudo = ft.Column(expand=True, spacing=15, scroll=ft.ScrollMode.AUTO)

    def aviso(texto, erro=False):
        page.snack_bar = ft.SnackBar(
            ft.Text(texto, color="white"),
            bgcolor="#A83232" if erro else "#176B4D"
        )
        page.snack_bar.open = True
        page.update()

    def campo(label, width=220):
        return ft.TextField(
            label=label, width=width, bgcolor="white", color="black",
            border_color="white"
        )

    def card(numero, texto):
        return ft.Container(
            width=190, height=120, bgcolor=CARD, border_radius=15, padding=18,
            content=ft.Column([
                ft.Text(str(numero).zfill(2), size=30,
                        weight=ft.FontWeight.BOLD, color=BRANCO),
                ft.Text(texto, color=BRANCO)
            ])
        )

    def dashboard():
        conteudo.controls.clear()
        conteudo.controls.extend([
            ft.Text("INÍCIO", size=30, weight=ft.FontWeight.BOLD, color=BRANCO),
            ft.Text(
                f"Bem-vindo, {usuario_logado[1] if usuario_logado else 'usuário'}",
                color="#CCCCCC"
            ),
            ft.Row([
                card(quantidade_computadores(), "Computadores"),
                card(chamados_abertos(), "Chamados Abertos"),
                card(chamados_atendimento(), "Em Atendimento"),
                card(chamados_resolvidos(), "Resolvidos"),
                card(quantidade_tecnicos(), "Técnicos")
            ], wrap=True, spacing=12),
            ft.Container(
                bgcolor=CARD, border_radius=15, padding=20,
                content=ft.Column([
                    ft.Text("Status do sistema", size=20,
                            weight=ft.FontWeight.BOLD, color=BRANCO),
                    ft.Text(
                        "Banco de dados conectado e atualizado em tempo real.",
                        color="#CCCCCC"
                    )
                ])
            )
        ])
        page.update()

    def computadores():
        conteudo.controls.clear()

        id_edicao = {"valor": None}
        patrimonio = campo("Patrimônio")
        modelo = campo("Modelo")
        laboratorio = campo("Laboratório")
        sistema_op = campo("Sistema Operacional")
        status = ft.Dropdown(
            label="Status", width=220, bgcolor="white", color="black",filled=True,fill_color=BRANCO,
            options=[ft.dropdown.Option(x) for x in ["Ativo", "Manutenção", "Inativo"]]
        )

        tabela = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("ID", color="white")),
                ft.DataColumn(ft.Text("Patrimônio", color="white")),
                ft.DataColumn(ft.Text("Modelo", color="white")),
                ft.DataColumn(ft.Text("Laboratório", color="white")),
                ft.DataColumn(ft.Text("Sistema", color="white")),
                ft.DataColumn(ft.Text("Status", color="white")),
                ft.DataColumn(ft.Text("Ações", color="white")),
            ],
            rows=[], border=ft.Border.all(1, ft.Colors.WHITE),
            horizontal_lines=ft.BorderSide(1, ft.Colors.WHITE),
            vertical_lines=ft.BorderSide(1, ft.Colors.WHITE)
        )

        def limpar():
            id_edicao["valor"] = None
            patrimonio.value = modelo.value = laboratorio.value = sistema_op.value = ""
            status.value = None

        def carregar():
            tabela.rows.clear()
            for item in buscar_computadores():
                tabela.rows.append(ft.DataRow(cells=[
                    ft.DataCell(ft.Text(str(item[0]), color="white")),
                    ft.DataCell(ft.Text(str(item[1]), color="white")),
                    ft.DataCell(ft.Text(str(item[2]), color="white")),
                    ft.DataCell(ft.Text(str(item[3]), color="white")),
                    ft.DataCell(ft.Text(str(item[4]), color="white")),
                    ft.DataCell(ft.Text(str(item[5]), color="white")),
                    ft.DataCell(ft.Row([
                        ft.IconButton(ft.Icons.EDIT, icon_color=VERDE,
                                      on_click=lambda e, x=item: editar(x)),
                        ft.IconButton(ft.Icons.DELETE, icon_color="#FF7070",
                                      on_click=lambda e, x=item: apagar(x[0]))
                    ]))
                ]))

        def editar(item):
            id_edicao["valor"] = item[0]
            patrimonio.value, modelo.value, laboratorio.value = item[1], item[2], item[3]
            sistema_op.value, status.value = item[4], item[5]
            btn.text = "Salvar alteração"
            page.update()

        def apagar(id_):
            try:
                excluir_computador(id_)
                carregar()
                aviso("Computador excluído.")
            except Exception as erro:
                aviso(f"Não foi possível excluir: {erro}", True)

        def salvar(e):
            if not patrimonio.value or not modelo.value or not laboratorio.value or not sistema_op.value:
                aviso("Preencha todos os campos do computador.", True)
                return
            try:
                if id_edicao["valor"] is None:
                    salvar_computador(patrimonio.value, modelo.value, laboratorio.value,
                                      sistema_op.value, status.value or "Ativo")
                    aviso("Computador cadastrado.")
                else:
                    atualizar_computador(id_edicao["valor"], patrimonio.value, modelo.value,
                                         laboratorio.value, sistema_op.value, status.value or "Ativo")
                    aviso("Computador atualizado.")
                limpar()
                btn.text = "Cadastrar computador"
                carregar()
                page.update()
            except Exception as erro:
                aviso(f"Erro: {erro}", True)

        btn = ft.ElevatedButton("Cadastrar computador", icon=ft.Icons.ADD, on_click=salvar)

        conteudo.controls.extend([
            ft.Text("COMPUTADORES", size=30, weight=ft.FontWeight.BOLD, color=BRANCO),
            ft.Row([patrimonio, modelo, laboratorio], wrap=True),
            ft.Row([sistema_op, status, btn], wrap=True),
            ft.Container(content=ft.Row([tabela], scroll=ft.ScrollMode.AUTO), expand=True)
        ])
        carregar()
        page.update()

    def chamados():
        conteudo.controls.clear()
        computadores_db, usuarios_db = dados_para_chamado()

        if not computadores_db:
            conteudo.controls.extend([
                ft.Text("CHAMADOS", size=30, weight=ft.FontWeight.BOLD, color=BRANCO),
                ft.Text("Cadastre pelo menos um computador antes de abrir um chamado.",
                        color="#CCCCCC")
            ])
            page.update()
            return

        computador = ft.Dropdown(
            label="Computador", width=300, bgcolor="white", color="black",filled=True,fill_color=BRANCO,
            options=[ft.dropdown.Option(str(x[0]), f"{x[1]} - {x[2]}")
                     for x in computadores_db]
        )
        usuario = ft.Dropdown(
            label="Usuário", width=250, bgcolor="white", color="black",filled=True,fill_color=BRANCO,
            options=[ft.dropdown.Option(str(x[0]), x[1]) for x in usuarios_db]
        )
        prioridade = ft.Dropdown(
            label="Prioridade", width=180, bgcolor="white", color="black",filled=True,fill_color=BRANCO,
            options=[ft.dropdown.Option(x) for x in ["Baixa", "Média", "Alta", "Urgente"]]
        )
        descricao = ft.TextField(
            label="Descrição do problema", multiline=True, width=500,
            height=80, bgcolor="white", color="black"
        )

        tabela = ft.DataTable(
            columns=[ft.DataColumn(ft.Text(x, color="white")) for x in
                     ["ID", "PC", "Patrimônio", "Usuário", "Descrição",
                      "Prioridade", "Status", "Data", "Ações"]],
            rows=[], border=ft.Border.all(1, ft.Colors.WHITE),
            horizontal_lines=ft.BorderSide(1, ft.Colors.WHITE),
            vertical_lines=ft.BorderSide(1, ft.Colors.WHITE)
        )

        def carregar():
            tabela.rows.clear()
            for item in buscar_chamados():
                tabela.rows.append(ft.DataRow(cells=[
                    ft.DataCell(ft.Text(str(item[0]), color="white")),
                    ft.DataCell(ft.Text(str(item[1]), color="white")),
                    ft.DataCell(ft.Text(str(item[2]), color="white")),
                    ft.DataCell(ft.Text(str(item[3]), color="white")),
                    ft.DataCell(ft.Text(str(item[4]), color="white")),
                    ft.DataCell(ft.Text(str(item[5]), color="white")),
                    ft.DataCell(ft.Text(str(item[6]), color="white")),
                    ft.DataCell(ft.Text(str(item[7]), color="white")),
                    ft.DataCell(ft.Row([
                        ft.IconButton(ft.Icons.PLAY_ARROW, tooltip="Em atendimento",
                                      icon_color=VERDE,
                                      on_click=lambda e, id_=item[0]:
                                      mudar_status(id_, "Em Atendimento")),
                        ft.IconButton(ft.Icons.CHECK, tooltip="Resolver",
                                      icon_color=VERDE,
                                      on_click=lambda e, id_=item[0]:
                                      resolver(id_)),
                        ft.IconButton(ft.Icons.DELETE, tooltip="Excluir",
                                      icon_color="#FF7070",
                                      on_click=lambda e, id_=item[0]:
                                      apagar(id_))
                    ]))
                ]))

        def cadastrar(e):
            if not computador.value or not descricao.value or not prioridade.value:
                aviso("Preencha computador, descrição e prioridade.", True)
                return
            try:
                salvar_chamado(int(computador.value),
                               int(usuario.value) if usuario.value else None,
                               descricao.value, prioridade.value)
                descricao.value = ""
                prioridade.value = None
                computador.value = None
                usuario.value = None
                carregar()
                aviso("Chamado cadastrado.")
                page.update()
            except Exception as erro:
                aviso(f"Erro ao cadastrar chamado: {erro}", True)

        def mudar_status(id_, novo_status):
            try:
                atualizar_status_chamado(id_, novo_status)
                carregar()
                aviso(f"Chamado atualizado para: {novo_status}")
            except Exception as erro:
                aviso(f"Erro: {erro}", True)

        def resolver(id_):
            tecnicos_db = buscar_tecnicos()
            if not tecnicos_db:
                aviso("Cadastre um técnico antes de resolver chamados.", True)
                return
            tecnico = ft.Dropdown(
                label="Técnico", width=300, bgcolor="white", color="black",
                options=[ft.dropdown.Option(str(x[0]), x[1]) for x in tecnicos_db]
            )
            solucao = ft.TextField(
                label="Solução aplicada", multiline=True, width=500,
                bgcolor="white", color="black"
            )

            def confirmar(e):
                if not tecnico.value or not solucao.value.strip():
                    aviso("Informe o técnico e a solução.", True)
                    return
                try:
                    salvar_solucao(id_, int(tecnico.value), solucao.value)
                    dlg.open = False
                    page.update()
                    carregar()
                    aviso("Chamado resolvido e solução registrada.")
                except Exception as erro:
                    aviso(f"Erro: {erro}", True)

            dlg = ft.AlertDialog(
                modal=True,
                title=ft.Text("Resolver chamado"),
                content=ft.Column([tecnico, solucao], tight=True),
                actions=[
                    ft.TextButton("Cancelar", on_click=lambda e: fechar()),
                    ft.ElevatedButton("Resolver", on_click=confirmar)
                ]
            )

            def fechar():
                dlg.open = False
                page.update()

            page.overlay.append(dlg)
            dlg.open = True
            page.update()

        def apagar(id_):
            try:
                excluir_chamado(id_)
                carregar()
                aviso("Chamado excluído.")
            except Exception as erro:
                aviso(f"Erro: {erro}", True)

        conteudo.controls.extend([
            ft.Text("CHAMADOS", size=30, weight=ft.FontWeight.BOLD, color=BRANCO),
            ft.Row([computador, usuario, prioridade], wrap=True),
            descricao,
            ft.ElevatedButton("Cadastrar chamado", icon=ft.Icons.ADD, on_click=cadastrar),
            ft.Container(content=ft.Row([tabela], scroll=ft.ScrollMode.AUTO), expand=True)
        ])
        carregar()
        page.update()

    def tecnicos():
        conteudo.controls.clear()
        id_edicao = {"valor": None}

        nome = campo("Nome", 210)
        email = campo("E-mail", 240)
        telefone = campo("Telefone", 170)
        especialidade = campo("Especialidade", 210)
        status = ft.Dropdown(
            label="Status", width=160, bgcolor="white", color="black",filled=True,fill_color=BRANCO,
            options=[ft.dropdown.Option(x) for x in ["Ativo", "Inativo", "Férias"]]
        )

        tabela = ft.DataTable(
            columns=[ft.DataColumn(ft.Text(x, color="white")) for x in
                     ["ID", "Nome", "E-mail", "Telefone", "Especialidade", "Status", "Ações"]],
            rows=[], border=ft.Border.all(1, ft.Colors.WHITE),
            horizontal_lines=ft.BorderSide(1, ft.Colors.WHITE),
            vertical_lines=ft.BorderSide(1, ft.Colors.WHITE)
        )

        def limpar():
            id_edicao["valor"] = None
            nome.value = email.value = telefone.value = especialidade.value = ""
            status.value = None

        def carregar():
            tabela.rows.clear()
            for item in buscar_tecnicos():
                tabela.rows.append(ft.DataRow(cells=[
                    ft.DataCell(ft.Text(str(item[0]), color="white")),
                    ft.DataCell(ft.Text(str(item[1]), color="white")),
                    ft.DataCell(ft.Text(str(item[2]), color="white")),
                    ft.DataCell(ft.Text(str(item[3] or ""), color="white")),
                    ft.DataCell(ft.Text(str(item[4] or ""), color="white")),
                    ft.DataCell(ft.Text(str(item[5]), color="white")),
                    ft.DataCell(ft.Row([
                        ft.IconButton(ft.Icons.EDIT, icon_color=VERDE,
                                      on_click=lambda e, x=item: editar(x)),
                        ft.IconButton(ft.Icons.DELETE, icon_color="#FF7070",
                                      on_click=lambda e, id_=item[0]: apagar(id_))
                    ]))
                ]))

        def editar(item):
            id_edicao["valor"] = item[0]
            nome.value, email.value, telefone.value = item[1], item[2], item[3] or ""
            especialidade.value, status.value = item[4] or "", item[5]
            btn.text = "Salvar alteração"
            page.update()

        def apagar(id_):
            try:
                excluir_tecnico(id_)
                carregar()
                aviso("Técnico excluído.")
            except Exception as erro:
                aviso("Não é possível excluir este técnico porque ele possui soluções "
                      "vinculadas a chamados.", True)

        def salvar(e):
            if not nome.value.strip() or not email.value.strip():
                aviso("Nome e e-mail são obrigatórios.", True)
                return
            try:
                if id_edicao["valor"] is None:
                    salvar_tecnico(nome.value, email.value, telefone.value,
                                   especialidade.value, status.value or "Ativo")
                    aviso("Técnico cadastrado.")
                else:
                    atualizar_tecnico(id_edicao["valor"], nome.value, email.value,
                                      telefone.value, especialidade.value,
                                      status.value or "Ativo")
                    aviso("Técnico atualizado.")
                limpar()
                btn.text = "Cadastrar técnico"
                carregar()
                page.update()
            except Exception as erro:
                aviso(f"Erro: {erro}", True)

        btn = ft.ElevatedButton("Cadastrar técnico", icon=ft.Icons.ADD, on_click=salvar)

        conteudo.controls.extend([
            ft.Text("TÉCNICOS", size=30, weight=ft.FontWeight.BOLD, color=BRANCO),
            ft.Text("Cadastro e gerenciamento dos técnicos.",
                    color="#CCCCCC"),
            ft.Row([nome, email, telefone], wrap=True),
            ft.Row([especialidade, status, btn], wrap=True),
            ft.Container(content=ft.Row([tabela], scroll=ft.ScrollMode.AUTO), expand=True)
        ])
        carregar()
        page.update()

    def logout(e=None):
        from Screens.Login import Login
        page.clean()
        Login(page)

    def menu_botao(texto, icone, funcao):
        return ft.Container(
            width=170, height=45, bgcolor="#F2F2F7", border_radius=25,
            content=ft.TextButton(
                texto, icon=icone,
                style=ft.ButtonStyle(color="#285B91"),
                on_click=lambda e: funcao()
            )
        )

    lateral = ft.Container(
        width=240, bgcolor=LATERAL, padding=30,
        content=ft.Column([
            ft.Text("TECHHELP", size=23, weight=ft.FontWeight.BOLD, color=VERDE),
            ft.Divider(color="#3A3854"),
            menu_botao("Início", ft.Icons.HOME, dashboard),
            menu_botao("PCs", ft.Icons.COMPUTER, computadores),
            menu_botao("Chamados", ft.Icons.WARNING, chamados),
            menu_botao("Técnicos", ft.Icons.PERSON, tecnicos),
            ft.Container(expand=True),
            menu_botao("Logout", ft.Icons.LOGOUT, logout)
        ], spacing=18, expand=True)
    )

    page.add(
        ft.Row(
            [
                lateral,
                ft.Container(expand=True, padding=35, content=conteudo)
            ],
            expand=True, spacing=0
        )
    )
    dashboard()