from flask import Flask
import os
from .database import conectar

app = Flask(__name__,
static_folder='app/static',
static_url_path='/static',
template_folder='app/templates')

os.makedirs("instance", exist_ok=True)

# criar as tabelas quando iniciar
conn = conectar()
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS marcas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    imagem TEXT NOT NULL,
    imagem_g TEXT NOT NULL
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS carros (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    imagem TEXT NOT NULL,
    marca_id INTEGER,
    FOREIGN KEY (marca_id) REFERENCES marcas(id)
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS modelos (
id INTEGER PRIMARY KEY AUTOINCREMENT,
nome TEXT NOT NULL,
preco_medio TEXT NOT NULL,
imagem TEXT NOT NULL,
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
manual TEXT,
modelo_id INTEGER,
FOREIGN KEY (modelo_id) REFERENCES modelos(id)
)
""")

conn.commit()
conn.close()

print("Tabelas verificadas/criadas com sucesso!")

from . import routes