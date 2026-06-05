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
    manual TEXT NULL,
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

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS avaliacoes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user TEXT NOT NULL,
    mensagem TEXT NOT NULL,
    nota INTEGER NOT NULL CHECK(nota >= 1 AND nota <= 5),
    modelo_id INTEGER,
    FOREIGN KEY (modelo_id) REFERENCES modelos(id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tipos_manutencao (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        icone TEXT NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE manutencao_itens (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    modelo_id INTEGER NOT NULL,
    tipo_manutencao_id INTEGER NOT NULL,

    item TEXT NOT NULL,
    intervalo TEXT NOT NULL,

    FOREIGN KEY (modelo_id) REFERENCES modelos(id),
    FOREIGN KEY (tipo_manutencao_id) REFERENCES tipos_manutencao(id)
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS manutencao_itens (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    manutencao_modelo_id INTEGER NOT NULL,

    item TEXT NOT NULL,
    intervalo TEXT NOT NULL,

    FOREIGN KEY (manutencao_modelo_id) REFERENCES manutencao_modelo(id)
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

def inserir_avaliacoes(user, mensagem, nota, modelo_id):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO fichas (user, mensagem, nota, modelo_id) VALUES (?, ?, ?, ?)",
        (user, mensagem, nota, modelo_id)
    )

    conn.commit()
    conn.close()
    
def inserir_tipo_manutencao(nome, icone):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO tipos_manutencao
    (nome, icone)
    VALUES (?, ?)
    """, (nome, icone))

    conn.commit()
    conn.close()


def inserir_manutencao_modelo(modelo_id, tipo_manutencao_id):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO manutencao_modelo
    (modelo_id, tipo_manutencao_id)
    VALUES (?, ?)
    """, (modelo_id, tipo_manutencao_id))

    conn.commit()
    conn.close()


def inserir_item_manutencao(manutencao_modelo_id, item, intervalo):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO manutencao_itens
    (manutencao_modelo_id, item, intervalo)
    VALUES (?, ?, ?)
    """, (manutencao_modelo_id, item, intervalo))

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
def listar_tipos_manutencao_modelo(modelo_id):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT DISTINCT
        tm.id,
        tm.nome,
        tm.icone

    FROM manutencao_itens mi

    JOIN tipos_manutencao tm
        ON tm.id = mi.tipo_manutencao_id

    WHERE mi.modelo_id = ?
    """, (modelo_id,))

    dados = cursor.fetchall()

    conn.close()

    return dados

# Listar Itens da Manutenção
def listar_itens_manutencao(modelo_id, tipo_manutencao_id):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT
        item,
        intervalo

    FROM manutencao_itens

    WHERE modelo_id = ?
    AND tipo_manutencao_id = ?
    """, (modelo_id, tipo_manutencao_id))

    dados = cursor.fetchall()

    conn.close()

    return dados

# Listar Manutenções com Itens
def listar_manutencoes_com_itens(modelo_id):

    tipos = listar_tipos_manutencao_modelo(modelo_id)

    resultado = []

    for tipo in tipos:

        resultado.append({
            "id": tipo["id"],
            "nome": tipo["nome"],
            "icone": tipo["icone"],
            "itens": listar_itens_manutencao(
                modelo_id,
                tipo["id"]
            )
        })

    return resultado

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