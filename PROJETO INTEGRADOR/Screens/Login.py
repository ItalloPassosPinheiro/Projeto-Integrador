import flet as ft
from Dados.Conexao import buscarlogin


def Login(page: ft.Page):
    page.title = "TechHelp"
    page.bgcolor = "#1F1C2E"
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
        color="Black",
        width=320,
        height=70,
        bgcolor="white",
        border_color="white",
        border_radius=5,
       
    )

    Senha = ft.TextField(
        label="Senha",
        password=True,
        can_reveal_password=True,
        width=320,
        height=70,
        bgcolor="White",
        border_color="White",
        color="Black",
        border_radius=5
    )

    alerta = ft.AlertDialog(
                modal=True,

                title=ft.Row(
                    [
                        ft.Icon(
                            ft.Icons.ERROR_OUTLINE,
                            color="#FF4D6D",
                            size=32
                        ),
                        ft.Text(
                            "Login inválido",
                            color="white",
                            size=22,
                            weight=ft.FontWeight.BOLD
                        ),
                    ],
                    spacing=10,
                ),

                content=ft.Text(
                    "Usuário ou senha incorretos.",
                    color="#D8D5E8",
                    size=16,
                ),

                actions=[
                    ft.ElevatedButton(
                        "Fechar",
                        on_click=fechar_alerta,
                        style=ft.ButtonStyle(
                            bgcolor="#00FF99",
                            color="black",
                            shape=ft.RoundedRectangleBorder(radius=8),
                        ),
                    )
                ],

                actions_alignment=ft.MainAxisAlignment.END,

                bgcolor="#2C2742",

                shape=ft.RoundedRectangleBorder(
                    radius=15
                ),

                open=False,
    )
    
    page.overlay.append(alerta)

    # ----------------------------
    # CARD LOGIN
    # ----------------------------

    login = ft.Container(
        width=500,
        height=450,
        bgcolor="#2C2742",
        border_radius=15,
        padding=30,
        shadow=ft.BoxShadow(
        blur_radius=25,
        spread_radius=1,
        color="#00000055",
        ),
        content=ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Text(
                    "LOGIN",
                    size=30,
                    weight=ft.FontWeight.BOLD,
                    color="#00FF99",
                ),

                ft.Container(height=20),

                ft.Column(
                    alignment=ft.MainAxisAlignment.CENTER,
                    controls=[Usuario,Senha,],
                ),

                ft.Row(alignment=ft.MainAxisAlignment.CENTER,controls=[       
                        
                        ft.TextButton(
                            "Cadastrar-Se",
                            style=ft.ButtonStyle(
                            color="White",
                            padding=0,),on_click=Cadastro
                        
                            
                        
                        ),
                        ft.Text(
                            "Recuperar senha?",
                            color="white",
                            size=15,
                        ),
                        ],spacing=100,
                        ),

                

                ft.Container(height=15),

                ft.ElevatedButton(
                    "Entrar",
                    width=300,
                    height=45,
                    on_click=logarnosistema,
                    style=ft.ButtonStyle(
                        bgcolor="#00FF99",
                        color="black",
                        shape=ft.RoundedRectangleBorder(radius=8),
                        
                    ),
                ),
            ],
        ),
    )

    # ----------------------------
    # FRASE E IMAGEM
    # ----------------------------
    Texto = ft.Column(
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
            ft.Text(
                "Faça login\n" \
                "E entre para o nosso time",
                size=60,
                weight=ft.FontWeight.W_700,
                color="#63FFC6",
                text_align=ft.TextAlign.CENTER,
            ),

            ft.Image(
                src="assets/Login.png",
                 width=400,
                 height=400,
                
            ),
                
        ],spacing=100,      
        
        alignment=ft.MainAxisAlignment.CENTER,
                
    )
    
    page.add(
        ft.Row(
            expand=True,
            alignment=ft.MainAxisAlignment.SPACE_AROUND,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                Texto,
                login,
            ],
        )
    )
