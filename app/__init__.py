from flask import Flask
import os
from .database import conectar

app = Flask(__name__)

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
    marca_id INTEGER,
    imagem TEXT NOT NULL,
    FOREIGN KEY (marca_id) REFERENCES marcas(id)
);
""")


conn.commit()
conn.close()

print("Tabelas verificadas/criadas com sucesso!")

from . import routes