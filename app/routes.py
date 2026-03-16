from . import app
from .database import conectar
import sqlite3
from flask import render_template, jsonify, request, redirect, url_for, flash
from .models import criar_tabelas, inserir_marcas, inserir_carros, inserir_modelos, inserir_fichas

@app.route("/")
def index():
    conn = conectar()
    marcas = conn.execute('SELECT * FROM marcas').fetchall()
    conn.close()
    return render_template("index.html", marcas=marcas)

@app.route("/marcas")
def marcas():
    conn = conectar()
    marcas = conn.execute('SELECT * FROM marcas').fetchall()
    conn.close()
    return render_template("marcas.html", marcas=marcas)

@app.route("/carros")
def carros():
    conn = conectar()
    carros = conn.execute('SELECT * FROM carros').fetchall()
    conn.close()
    return render_template("carros.html", carros=carros)

@app.route("/criar_tabelas")
def criar_tabela():
    criar_tabelas()
    return "Tabelas Criadas!"

#inserir_marcas("Nome da Marca", "Nome da Marca Padrão.png", "Nome da Marca Cinza.png")
#Exemplo na Prática: inserir_marcas("GWM", "gwm_logo.png", "gwm_logo_g.png")
@app.route("/inserir_marca", methods=["GET", "POST"])
def inserir_marca():
    inserir_marcas("BYD", "byd_logo.png", "byd_logo_g.png")
    return "Marca Inserida!"

#inserir_carros("Nome do carro", "Nome do carro.png", <id da marca>)
#Exemplo na Prática: inserir_carros("Haval", "haval.png", 1)
@app.route("/inserir_carro", methods=["GET", "POST"])
def inserir_carro():
    inserir_carros("Song", "song.png", 2)
    return "Carro Inserido!"

#inserir_carros("Nome do modelo", "<preço médio>", "Nome do modelo.png", <id do carro>)
#Exemplo na Prática: inserir_carros("Haval H6", "??????.00", "haval_h6.png", 1)
@app.route("/inserir_modelo", methods=["GET", "POST"])
def inserir_modelo():
    inserir_modelos("Haval H6", "??????.00", "haval_h6.png", 1)
    return "Modelo de Carro Inserido!"

#inserir_carros("ano", "tipo_motor", "descricao_motor", "autonomia", "potencia", "porte", "dimensoes", "lugares", "cambio", "velocidade_maxima", <id do modelo>)
#Exemplo na Prática: inserir_carros("ano", "tipo_motor", "descricao_motor", "autonomia", "potencia", "porte", "dimensoes", "lugares", "cambio", "velocidade_maxima", <id do modelo>)
@app.route("/inserir_fichas", methods=["GET", "POST"])
def inserir_ficha():
    inserir_fichas("ano", "tipo_motor", "descricao_motor", "autonomia", "potencia", "porte", "dimensoes", "lugares", "cambio", "velocidade_maxima", 1)
    return "Modelo de Carro Inserido!"