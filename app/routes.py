from . import app
from .database import conectar
import sqlite3
from flask import render_template, jsonify, request, redirect, url_for, flash
from .models import criar_tabelas, inserir_marcas, inserir_carros

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

@app.route("/inserir_marca")
def inserir_marca():
    inserir_marcas("Citroën", "citroen_logo.png", "citroen_logo_g.png")
    return "Marca Inserida!"

@app.route("/inserir_carro")
def inserir_carro():
    inserir_carros("Onix", 1, "onix.png")
    return "Carro Inserido!"