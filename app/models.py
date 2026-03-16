import sqlite3
from .database import conectar

# CRIAR TABELAS
def criar_tabelas():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS marcas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    imagem TEXT NOT NULL,
    imagem_g TEXT NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS carros (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    marca_id INTEGER,
    imagem TEXT NOT NULL,
    FOREIGN KEY (marca_id) REFERENCES marcas(id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS modelos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    imagem TEXT NOT NULL,
    preco_medio TEXT NOT NULL,
    carro_id INTEGER,
    FOREIGN KEY (carro_id) REFERENCES carros(id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS fichas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ano TEXT NULL,
    tipo_motor TEXT NOT NULL,
    descricao_motor TEXT NULL,
    autonomia TEXT NULL,
    potencia TEXT NULL,
    porte TEXT NULL,
    dimensoes TEXT NULL,
    lugares TEXT NULL,
    cambio TEXT NULL,
    velocidade_maxima TEXT NULL,
    modelo_id INTEGER,
    FOREIGN KEY (modelo_id) REFERENCES modelos(id)
    )
    """)

    conn.commit()
    conn.close()

# INSERIR DADOS
def inserir_marcas(nome, imagem, imagem_g):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO marcas (nome, imagem, imagem_g) VALUES (?, ?, ?)",
        (nome, imagem, imagem_g)
    )

    conn.commit()
    conn.close()


def inserir_carros(nome, imagem, marca_id):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO carros (nome, imagem, marca_id) VALUES (?, ?, ?)",
        (nome, imagem, marca_id)
    )

    conn.commit()
    conn.close()

def inserir_modelos(nome, preco_medio, imagem, carro_id):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO modelos (nome, preco_medio, imagem, carro_id) VALUES (?, ?, ?, ?)",
        (nome, preco_medio, imagem, carro_id)
    )

    conn.commit()
    conn.close()

def inserir_fichas(ano, tipo_motor, descricao_motor, autonomia, potencia, porte, dimensoes, lugares, cambio, velocidade_maxima, modelo_id):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO fichas (ano, tipo_motor, descricao_motor, autonomia, potencia, porte, dimensoes, lugares, cambio, velocidade_maxima, modelo_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (ano, tipo_motor, descricao_motor, autonomia, potencia, porte, dimensoes, lugares, cambio, velocidade_maxima, modelo_id)
    )

    conn.commit()
    conn.close()

# LISTAR DADOS
def listar_carros():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT carros.id, carros.nome, carros.ano, marcas.nome
    FROM carros
    JOIN marcas ON carros.marca_id = marcas.id
    """)

    dados = cursor.fetchall()

    conn.close()
    return dados

# DELETAR
def deletar_carro(id):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM carros WHERE id = ?",
        (id,)
    )

    conn.commit()
    conn.close()