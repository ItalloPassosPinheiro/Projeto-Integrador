from Dados.Conexao import inicializar_banco

def criar_tabelas():
    inicializar_banco()

if __name__ == "__main__":
    criar_tabelas()
    print("Banco de dados pronto.")
