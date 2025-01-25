import sqlite3


def inicializar_bd():
    """Inicializa o banco de dados e cria a tabela, caso não exista."""
    conn = sqlite3.connect("cartas.db")
    cursor = conn.cursor()
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS baralho (
           id INTEGER PRIMARY KEY AUTOINCREMENT,
           nome TEXT
        )"""
    )
    conn.commit()
    conn.close()


def salvar_carta(nome):
    """Salva uma carta no banco de dados."""
    conn = sqlite3.connect("cartas.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO baralho (nome) VALUES (?)", (nome,))
    conn.commit()
    conn.close()


def carregar_cartas():
    """Carrega as cartas do banco de dados."""
    cartas = []
    conn = sqlite3.connect("cartas.db")
    cursor = conn.cursor()
    cursor.execute("SELECT nome FROM baralho")
    resultado = cursor.fetchall()
    for carta in resultado:
        cartas.append(carta[0])
    conn.close()
    return cartas


def excluir_todas_as_cartas():
    """Exclui todas as cartas do banco de dados."""
    conn = sqlite3.connect("cartas.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM baralho")  # Deleta todas as cartas da tabela
    conn.commit()
    conn.close()

