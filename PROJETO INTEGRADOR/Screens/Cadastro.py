import flet as ft
from Dados.Conexao import salvar_usuario


FUNDO = "#F5F7FA"
CARD = "#174A7C"
AZUL_ESCURO = "#12355B"
AZUL = "#1E5AA8"
AZUL_CLARO = "#2F75C9"
TEXTO = "#1F2937"
CINZA = "#64748B"
BORDA = "#D6DCE5"
VERDE = "#198754"
VERMELHO = "#C62828"


def Cadastro(page: ft.Page):
    page.title = "TechHelp - Cadastro"
    page.bgcolor = FUNDO
    page.padding = 0
    page.window.maximized = True

    nome = ft.TextField(
        label="Nome",
        width=300,
        bgcolor="#FFFFFF",
        color=TEXTO,
        border_color=BORDA
    )

    email = ft.TextField(
        label="E-mail",
        width=300,
        bgcolor="#FFFFFF",
        color=TEXTO,
        border_color=BORDA
    )

    senha = ft.TextField(
        label="Senha",
        width=300,
        bgcolor="#FFFFFF",
        color=TEXTO,
        border_color=BORDA,
        password=True,
        can_reveal_password=True
    )



    mensagem = ft.Text("", size=13)

    def voltar(e):
        from Screens.Login import Login
        page.clean()
        Login(page)

    def cadastrar(e):
        if not nome.value.strip() or not email.value.strip() or not senha.value:
            mensagem.value = "Preencha todos os campos."
            mensagem.color = VERMELHO
            page.update()
            return

        try:
            salvar_usuario(
                nome.value,
                email.value,
                senha.value,
                "Usuário"
            )

            mensagem.value = "Cadastro realizado! Você já pode entrar."
            mensagem.color = VERDE

            nome.value = email.value = senha.value = ""

            page.update()

        except Exception as erro:
            mensagem.value = (
                "Não foi possível cadastrar. "
                "Verifique se o e-mail já está cadastrado."
            )

            mensagem.color = VERMELHO
            page.update()

    card = ft.Container(
        width=500,
        height=480,
        padding=35,
        bgcolor=CARD,
        border_radius=15,
        content=ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=12,
            controls=[
                ft.Text(
                    "CADASTRO",
                    size=30,
                    weight=ft.FontWeight.BOLD,
                    color="#FFFFFF"
                ),

                nome,
                email,
                senha,
                mensagem,

                ft.Row(
                    width=300,
                    controls=[
                        ft.TextButton(
                            "Voltar para login",
                            on_click=voltar,
                            style=ft.ButtonStyle(
                                color="#FFFFFF"
                            )
                        )
                    ]
                ),

                ft.ElevatedButton(
                    "CADASTRAR",
                    width=300,
                    height=45,
                    on_click=cadastrar,
                    style=ft.ButtonStyle(
                        bgcolor=AZUL_CLARO,
                        color="#FFFFFF",
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
                        ft.Text(
                            "Faça seu cadastro\n"
                            "E faça parte da nossa equipe",
                            size=52,
                            weight=ft.FontWeight.W_700,
                            color=AZUL_ESCURO,
                            text_align=ft.TextAlign.CENTER
                        ),

                        ft.Image(
                            src="assets/logol.png",
                            width=550,
                            height=550
                        )
                    ]
                ),

                card
            ]
        )
    )
