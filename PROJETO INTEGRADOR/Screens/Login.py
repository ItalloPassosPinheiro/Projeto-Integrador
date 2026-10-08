import flet as ft
from Dados.Conexao import buscarlogin


def Login(page: ft.Page):
    page.title = "TechHelp"
    page.bgcolor = "#F5F7FA"
    page.padding = 0
    page.window.maximized = True
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    def fechar_alerta(e):
        alerta.open = False
        page.update()

    def logarnosistema(e):
        resultado = buscarlogin(
            Usuario.value,
            Senha.value
        )

        if resultado:
            from Screens.Sistema import sistema
            page.clean()
            sistema(page)
        else:
            alerta.open = True
            Usuario.value = ""
            Senha.value = ""
            page.update()

    def Cadastro(e):
        from Screens.Cadastro import Cadastro
        page.clean()
        Cadastro(page)
        return

    Usuario = ft.TextField(
        label="Usuário",
        color="#1F2937",
        width=320,
        height=70,
        bgcolor="#FFFFFF",
        border_color="#D6DCE5",
        border_radius=5,
    )

    Senha = ft.TextField(
        label="Senha",
        password=True,
        can_reveal_password=True,
        width=320,
        height=70,
        bgcolor="#FFFFFF",
        border_color="#D6DCE5",
        color="#1F2937",
        border_radius=5
    )

    alerta = ft.AlertDialog(
        modal=True,
        title=ft.Row(
            [
                ft.Icon(
                    ft.Icons.ERROR_OUTLINE,
                    color="#C62828",
                    size=32
                ),
                ft.Text(
                    "Login inválido",
                    color="#1F2937",
                    size=22,
                    weight=ft.FontWeight.BOLD
                ),
            ],
            spacing=10,
        ),
        content=ft.Text(
            "Usuário ou senha incorretos.",
            color="#64748B",
            size=16
        ),
        actions=[
            ft.ElevatedButton(
                "Fechar",
                on_click=fechar_alerta,
                style=ft.ButtonStyle(
                    bgcolor="#2F75C9",
                    color="#FFFFFF",
                    shape=ft.RoundedRectangleBorder(radius=8),
                ),
            )
        ],
        actions_alignment=ft.MainAxisAlignment.END,
        bgcolor="#FFFFFF",
        shape=ft.RoundedRectangleBorder(radius=15),
        open=False,
    )

    page.overlay.append(alerta)

    login = ft.Container(
        width=500,
        height=450,
        bgcolor="#174A7C",
        border_radius=15,
        padding=30,
        shadow=ft.BoxShadow(
            blur_radius=25,
            spread_radius=1,
            color="#00000030",
        ),
        content=ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Text(
                    "LOGIN",
                    size=30,
                    weight=ft.FontWeight.BOLD,
                    color="#FFFFFF"
                ),

                ft.Container(height=20),

                ft.Column(
                    alignment=ft.MainAxisAlignment.CENTER,
                    controls=[
                        Usuario,
                        Senha,
                    ],
                ),

                ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER,
                    controls=[
                        ft.TextButton(
                            "Cadastrar-Se",
                            style=ft.ButtonStyle(
                                color="#FFFFFF",
                                padding=0
                            ),
                            on_click=Cadastro
                        ),

                        ft.Text(
                            "Recuperar senha?",
                            color="#FFFFFF",
                            size=15
                        ),
                    ],
                    spacing=100,
                ),

                ft.Container(height=15),

                ft.ElevatedButton(
                    "Entrar",
                    width=300,
                    height=45,
                    on_click=logarnosistema,
                    style=ft.ButtonStyle(
                        bgcolor="#2F75C9",
                        color="#FFFFFF",
                        shape=ft.RoundedRectangleBorder(radius=8),
                    ),
                ),
            ],
        ),
    )

    page.add(ft.Row(
            expand=True,
            alignment=ft.MainAxisAlignment.SPACE_AROUND,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Column(
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    alignment=ft.MainAxisAlignment.CENTER,
                    controls=[
                        ft.Text(
                            "Faça login\n"
                            "E entre para o nosso time",
                            size=52,
                            weight=ft.FontWeight.W_700,
                            color="#12355B",
                            text_align=ft.TextAlign.CENTER
                        ),

                        ft.Image(
                            src="assets/logol.png",
                            width=550,
                            height=550
                        )
                    ]
                ),

                login
            ]
        )
    )
