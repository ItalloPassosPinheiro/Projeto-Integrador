import flet as ft
from Dados.Conexao import salvar_usuario


FUNDO = "#1F1C2E"
CARD = "#2C2742"
VERDE = "#00FF99"


def Cadastro(page: ft.Page):
    page.title = "TechHelp - Cadastro"
    page.bgcolor = FUNDO
    page.padding = 0
    page.window.maximized = True

    nome = ft.TextField(label="Nome", width=300, bgcolor="white", color="black")
    email = ft.TextField(label="E-mail", width=300, bgcolor="white", color="black")
    senha = ft.TextField(
        label="Senha", width=300, bgcolor="white", color="black",
        password=True, can_reveal_password=True
    )
    mensagem = ft.Text("", size=13)

    def voltar(e):
        from Screens.Login import Login
        page.clean()
        Login(page)

    def cadastrar(e):
        if not nome.value.strip() or not email.value.strip() or not senha.value:
            mensagem.value = "Preencha todos os campos."
            mensagem.color = "#FF6B6B"
            page.update()
            return
        try:
            salvar_usuario(nome.value, email.value, senha.value, "Usuário")
            mensagem.value = "Cadastro realizado! Você já pode entrar."
            mensagem.color = VERDE
            nome.value = email.value = senha.value = ""
            page.update()
        except Exception as erro:
            mensagem.value = (
                "Não foi possível cadastrar. "
                "Verifique se o e-mail já está cadastrado."
            )
            mensagem.color = "#FF6B6B"
            page.update()

    card = ft.Container(
        width=500,height=480, padding=35, bgcolor=CARD, border_radius=15,
        content=ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=12,
            controls=[
                ft.Text("CADASTRO", size=30, weight=ft.FontWeight.BOLD, color=VERDE),
                nome, email, senha, mensagem,
                ft.Row(
                    width=300,
                    controls=[
                        ft.TextButton("Voltar para login", on_click=voltar,
                                      style=ft.ButtonStyle(color="white"))
                    ]
                ),
                ft.ElevatedButton(
                    "CADASTRAR", width=300, height=45, on_click=cadastrar,
                    style=ft.ButtonStyle(
                        bgcolor=VERDE, color="black",
                        shape=ft.RoundedRectangleBorder(radius=8)
                    )
                )
            ]
        )
    )

    page.add(
        ft.Row(
            expand=True,
            alignment=ft.MainAxisAlignment.SPACE_AROUND,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Column(
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    alignment=ft.MainAxisAlignment.CENTER,
                    controls=[
                        ft.Text("Faça seu cadastro\nE faça parte da nossa equipe",
                                size=52, weight=ft.FontWeight.W_700,
                                color="#63FFC6", text_align=ft.TextAlign.CENTER),
                        ft.Image(src="assets/Login.png", width=400, height=400)
                    ]
                ),
                card
            ]
        )
    )
