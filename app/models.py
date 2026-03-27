import sqlite3
from .database import conectar

# Criar Tabelas
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
    ano TEXT,
    autonomia TEXT,
    potencia TEXT,
    porte TEXT,
    dimensoes TEXT,
    lugares TEXT,
    cambio TEXT,
    velocidade_maxima TEXT,
    modelo_id INTEGER,
    motor_id INTEGER,
    FOREIGN KEY (modelo_id) REFERENCES modelos(id),
    FOREIGN KEY (motor_id) REFERENCES motores(id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS motores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tipo_motor TEXT NOT NULL,
    desc_motor TEXT
    )
    """)

    conn.commit()
    conn.close()

# Inserir Dados
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

# Listar Dados
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

# Listar Carros por Marca
def listar_carro_por_marca(marca_id):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT carros.id, carros.nome, marcas.nome
    FROM carros
    JOIN marcas ON carros.marca_id = marcas.id
    WHERE marca_id = ?
    """, (marca_id,))

    dados = cursor.fetchall()
    conn.close()

    return dados

# Listar Modelos por Carro
def listar_modelos_por_carro(carro_id):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT modelos.id, modelos.nome, modelos.imagem
    FROM modelos
    JOIN carros ON modelos.carro_id = carros.id
    WHERE carro_id = ?
    """, (carro_id,))

    dados = cursor.fetchall()
    conn.close()

    return dados

# Listar Ficha por Modelo

# Listar Manual por Modelo

# Listar Manutenções por Modelo

# Deletar
def deletar_carro(id):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM carros WHERE id = ?",
        (id,)
    )

    conn.commit()
    conn.close()