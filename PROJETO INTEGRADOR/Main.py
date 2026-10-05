import flet as ft
from Dados.Conexao import inicializar_banco
from Screens.Login import Login


def main(page: ft.Page):
    inicializar_banco()
    page.clean()
    Login(page)


if __name__ == "__main__":
    ft.run(main)
