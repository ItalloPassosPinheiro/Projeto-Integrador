import sqlite3
from datetime import datetime
from pathlib import Path

BASE = Path(__file__).resolve().parent
BANCO = BASE / "banco.db"

def buscarlogin(emaildousuario, senhadousuario):
    inicializar_banco()

    with conectar() as con:
        cs = con.cursor()

        cs.execute("""
            SELECT email, senha
            FROM usuarios
            WHERE email = ? AND senha = ?
        """, (emaildousuario, senhadousuario))

        resultado = cs.fetchone()

    return resultado is not None

def conectar():
    conexao = sqlite3.connect(BANCO)
    conexao.execute("PRAGMA foreign_keys = ON")
    return conexao


def inicializar_banco():
    with conectar() as conexao:
        conexao.executescript("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            senha TEXT NOT NULL,
            tipo TEXT NOT NULL DEFAULT 'Usuário'
        );

        CREATE TABLE IF NOT EXISTS tecnicos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            telefone TEXT,
            especialidade TEXT,
            status TEXT NOT NULL DEFAULT 'Ativo'
        );

        CREATE TABLE IF NOT EXISTS computadores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patrimonio TEXT NOT NULL UNIQUE,
            modelo TEXT NOT NULL,
            laboratorio TEXT NOT NULL,
            sistema_operacional TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'Ativo'
        );

        CREATE TABLE IF NOT EXISTS chamados (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            computador_id INTEGER NOT NULL,
            usuario_id INTEGER,
            descricao TEXT NOT NULL,
            prioridade TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'Aberto',
            data_abertura TEXT NOT NULL,
            data_fechamento TEXT,
            FOREIGN KEY (computador_id) REFERENCES computadores(id)
                ON UPDATE CASCADE ON DELETE CASCADE,
            FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
                ON UPDATE CASCADE ON DELETE SET NULL
        );

        CREATE TABLE IF NOT EXISTS solucoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            chamado_id INTEGER NOT NULL,
            tecnico_id INTEGER NOT NULL,
            descricao TEXT NOT NULL,
            data TEXT NOT NULL,
            FOREIGN KEY (chamado_id) REFERENCES chamados(id)
                ON UPDATE CASCADE ON DELETE CASCADE,
            FOREIGN KEY (tecnico_id) REFERENCES tecnicos(id)
                ON UPDATE CASCADE ON DELETE RESTRICT
        );
        """)


# ---------------- USUÁRIOS ----------------

def salvar_usuario(nome, email, senha, tipo="Usuário"):
    with conectar() as c:
        c.execute(
            "INSERT INTO usuarios(nome,email,senha,tipo) VALUES(?,?,?,?)",
            (nome.strip(), email.strip().lower(), senha, tipo)
        )


def autenticar_usuario(login, senha):
    with conectar() as c:
        return c.execute("""
            SELECT id, nome, email, tipo
            FROM usuarios
            WHERE (lower(email)=lower(?) OR lower(nome)=lower(?))
              AND senha=?
            LIMIT 1
        """, (login.strip(), login.strip(), senha)).fetchone()


def buscar_usuarios():
    with conectar() as c:
        return c.execute("""
            SELECT id,nome,email,tipo FROM usuarios ORDER BY id DESC
        """).fetchall()


# ---------------- TÉCNICOS ----------------

def salvar_tecnico(nome, email, telefone, especialidade, status="Ativo"):
    with conectar() as c:
        c.execute("""
            INSERT INTO tecnicos(nome,email,telefone,especialidade,status)
            VALUES(?,?,?,?,?)
        """, (nome.strip(), email.strip().lower(), telefone.strip(),
              especialidade.strip(), status))


def atualizar_tecnico(id_, nome, email, telefone, especialidade, status):
    with conectar() as c:
        c.execute("""
            UPDATE tecnicos
            SET nome=?,email=?,telefone=?,especialidade=?,status=?
            WHERE id=?
        """, (nome.strip(), email.strip().lower(), telefone.strip(),
              especialidade.strip(), status, id_))


def excluir_tecnico(id_):
    with conectar() as c:
        c.execute("DELETE FROM tecnicos WHERE id=?", (id_,))


def buscar_tecnicos():
    with conectar() as c:
        return c.execute("""
            SELECT id,nome,email,telefone,especialidade,status
            FROM tecnicos ORDER BY id DESC
        """).fetchall()


# ---------------- COMPUTADORES ----------------

def salvar_computador(patrimonio, modelo, laboratorio, sistema_operacional, status):
    with conectar() as c:
        c.execute("""
            INSERT INTO computadores
            (patrimonio,modelo,laboratorio,sistema_operacional,status)
            VALUES(?,?,?,?,?)
        """, (patrimonio.strip(), modelo.strip(), laboratorio.strip(),
              sistema_operacional.strip(), status))


def atualizar_computador(id_, patrimonio, modelo, laboratorio, sistema_operacional, status):
    with conectar() as c:
        c.execute("""
            UPDATE computadores
            SET patrimonio=?,modelo=?,laboratorio=?,sistema_operacional=?,status=?
            WHERE id=?
        """, (patrimonio.strip(), modelo.strip(), laboratorio.strip(),
              sistema_operacional.strip(), status, id_))


def excluir_computador(id_):
    with conectar() as c:
        c.execute("DELETE FROM computadores WHERE id=?", (id_,))


def buscar_computadores():
    with conectar() as c:
        return c.execute("""
            SELECT id,patrimonio,modelo,laboratorio,sistema_operacional,status
            FROM computadores ORDER BY id DESC
        """).fetchall()


# ---------------- CHAMADOS ----------------

def salvar_chamado(computador_id, usuario_id, descricao, prioridade):
    data = datetime.now().strftime("%d/%m/%Y %H:%M")
    with conectar() as c:
        c.execute("""
            INSERT INTO chamados
            (computador_id,usuario_id,descricao,prioridade,status,data_abertura)
            VALUES(?,?,?,?,?,?)
        """, (computador_id, usuario_id, descricao.strip(), prioridade,
              "Aberto", data))


def atualizar_status_chamado(id_, status):
    fechamento = datetime.now().strftime("%d/%m/%Y %H:%M") if status == "Resolvido" else None
    with conectar() as c:
        c.execute("""
            UPDATE chamados
            SET status=?, data_fechamento=?
            WHERE id=?
        """, (status, fechamento, id_))


def excluir_chamado(id_):
    with conectar() as c:
        c.execute("DELETE FROM chamados WHERE id=?", (id_,))


def buscar_chamados():
    with conectar() as c:
        return c.execute("""
            SELECT
                chamados.id,
                computadores.id,
                computadores.patrimonio,
                COALESCE(usuarios.nome,'Não informado'),
                chamados.descricao,
                chamados.prioridade,
                chamados.status,
                chamados.data_abertura
            FROM chamados
            INNER JOIN computadores ON chamados.computador_id=computadores.id
            LEFT JOIN usuarios ON chamados.usuario_id=usuarios.id
            ORDER BY chamados.id DESC
        """).fetchall()


def dados_para_chamado():
    with conectar() as c:
        computadores = c.execute(
            "SELECT id,patrimonio,modelo FROM computadores ORDER BY patrimonio"
        ).fetchall()
        usuarios = c.execute(
            "SELECT id,nome,email FROM usuarios ORDER BY nome"
        ).fetchall()
        return computadores, usuarios


# ---------------- SOLUÇÕES ----------------

def salvar_solucao(chamado_id, tecnico_id, descricao):
    data = datetime.now().strftime("%d/%m/%Y %H:%M")
    with conectar() as c:
        c.execute("""
            INSERT INTO solucoes(chamado_id,tecnico_id,descricao,data)
            VALUES(?,?,?,?)
        """, (chamado_id, tecnico_id, descricao.strip(), data))
        c.execute("""
            UPDATE chamados
            SET status='Resolvido', data_fechamento=?
            WHERE id=?
        """, (data, chamado_id))


# ---------------- DASHBOARD ----------------

def quantidade_computadores():
    with conectar() as c:
        return c.execute("SELECT COUNT(*) FROM computadores").fetchone()[0]


def chamados_abertos():
    with conectar() as c:
        return c.execute(
            "SELECT COUNT(*) FROM chamados WHERE status='Aberto'"
        ).fetchone()[0]


def chamados_atendimento():
    with conectar() as c:
        return c.execute(
            "SELECT COUNT(*) FROM chamados WHERE status='Em Atendimento'"
        ).fetchone()[0]


def chamados_resolvidos():
    with conectar() as c:
        return c.execute(
            "SELECT COUNT(*) FROM chamados WHERE status='Resolvido'"
        ).fetchone()[0]


def quantidade_tecnicos():
    with conectar() as c:
        return c.execute("SELECT COUNT(*) FROM tecnicos").fetchone()[0]
