from . import app
from .database import conectar
import sqlite3
from flask import render_template, jsonify, request, redirect, url_for, flash
from .models import criar_tabelas, inserir_marcas, inserir_carros, inserir_modelos, inserir_fichas, listar_modelos_por_carro

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
    marca_id = request.args.get("marca_id", type=int)

    conn = conectar()
    marcas = conn.execute('SELECT * FROM marcas').fetchall()
    carros = conn.execute('SELECT * FROM carros').fetchall()

    if marca_id:
        carros = conn.execute("SELECT * FROM carros WHERE marca_id = ?",(marca_id,)).fetchall()
    else:
        carros = conn.execute("SELECT * FROM carros").fetchall()
    conn.close()

    modelos_por_carro = {}

    for carro in carros:
        modelos_por_carro[carro["id"]] = listar_modelos_por_carro(carro["id"])

    return render_template("carros.html", carros=carros, marcas=marcas, modelos_por_carro = modelos_por_carro, marca_ativa=marca_id)

@app.route("/api/carros")
def api_carros():
    conn = conectar()
    carros = conn.execute('SELECT * FROM carros').fetchall()
    conn.close()

    modelos_por_carro = {}

    for carro in carros:
        modelos_por_carro[carro["id"]] = listar_modelos_por_carro(carro["id"])
    
    return render_template("partials/_carros.html", carros = carros, modelos_por_carro = modelos_por_carro)

@app.route("/api/carros/<int:marca_id>")
def api_carros_por_marca(marca_id):
    conn = conectar()
    carros = conn.execute('SELECT * FROM carros WHERE marca_id = ?', (marca_id,)).fetchall()
    conn.close()

    modelos_por_carro = {}

    for carro in carros:
        modelos_por_carro[carro["id"]] = listar_modelos_por_carro(carro["id"])
    
    return render_template("partials/_carros.html", carros = carros, modelos_por_carro = modelos_por_carro)

@app.route("/modelo/<int:id>")
def carros_por_modelo(id):
    conn = conectar()
    modelos = conn.execute('SELECT * FROM modelos WHERE id = ?', (id,)).fetchall()
    conn.close()
    return render_template("modelo.html", modelos=modelos)

@app.route("/api/modelo/<int:id>/<tipo>")
def abas_modelo(id,tipo):
    conn = conectar()

    modelos = conn.execute('SELECT * FROM modelos WHERE id = ?', (id,)).fetchall()

    conn.close()

    if tipo == "geral":
        return render_template("partials/_geral.html", modelos = modelos) 
    
    elif tipo == "ficha":
        conn = conectar()

        fichas = conn.execute("""
        SELECT f.*, m.tipo_motor, m.desc_motor
        FROM fichas f
        LEFT JOIN motores m ON f.motor_id = m.id
        WHERE f.modelo_id = ?
        """, (id,)).fetchall()

        conn.close()

        return render_template("partials/_ficha.html", modelos=modelos, fichas=fichas)
    
    elif tipo == "avaliacao":
        conn = conectar()

        avaliacoes = conn.execute("""
        SELECT * FROM avaliacoes
        WHERE modelo_id = ?
        """, (id,)).fetchall()

        conn.close()
    
        return render_template("partials/_avaliacao.html", modelos = modelos, avaliacoes = avaliacoes)

@app.route("/criar_tabelas")
def criar_tabela():
    criar_tabelas()
    return "Tabelas Criadas!"

# inserir_marcas("Nome da Marca", "Nome da Marca Padrão.png", "Nome da Marca Cinza.png")
# Exemplo na Prática: inserir_marcas("GWM", "gwm_logo.png", "gwm_logo_g.png")
@app.route("/inserir_marca", methods=["GET", "POST"])
def inserir_marca():
    inserir_marcas("BYD", "byd_logo.png", "byd_logo_g.png")
    return "Marca Inserida!"

# inserir_carros("Nome do carro", "Nome do carro.png", <id da marca>)
# Exemplo na Prática: inserir_carros("Haval", "haval.png", 1)
@app.route("/inserir_carro", methods=["GET", "POST"])
def inserir_carro():
    inserir_carros("Song", "song.png", 1)
    return "Carro Inserido!"

# inserir_carros("Nome do modelo", "<preço médio>", "Nome do modelo.png", <id do carro>)
# Exemplo na Prática: inserir_carros("Haval H6", "??????.00", "haval_h6.png", 1)
@app.route("/inserir_modelo", methods=["GET", "POST"])
def inserir_modelo():
    inserir_modelos("Song Plus Premium", "299.800.00", "song_plus_premium.png", 2)
    return "Modelo de Carro Inserido!"

@app.route("/inserir_ficha", methods=["POST"])
def inserir_ficha():
    conn = conectar()

    tipo_motor = request.form["tipo_motor"]
    desc_motor = request.form["desc_motor"]

    ano = request.form["ano"]
    autonomia = request.form["autonomia"]
    potencia = request.form["potencia"]
    porte = request.form["porte"]
    dimensoes = request.form["dimensoes"]
    lugares = request.form["lugares"]
    cambio = request.form["cambio"]
    velocidade_maxima = request.form["velocidade_maxima"]
    modelo_id = request.form["modelo_id"]

    motor = conn.execute("SELECT id FROM motores WHERE tipo_motor = ?", (tipo_motor,)).fetchone()

    # inserir motor caso ele não exista
    if motor is None:
        conn.execute("INSERT INTO motores (tipo_motor, desc_motor) VALUES (?, ?)", (tipo_motor, desc_motor))

        motor_id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]
    else:
        motor_id = motor["id"]

    # inserir ficha
    conn.execute("""
    INSERT INTO fichas (
    ano, autonomia, potencia, porte, dimensoes, lugares, cambio, velocidade_maxima, modelo_id, motor_id) 
    VALUES (?, ?, ?, ?)""", (ano, autonomia, potencia, porte, dimensoes, lugares, cambio, velocidade_maxima, modelo_id, motor_id))

    conn.commit()
    conn.close()

    return redirect("/carros")

@app.route("/aba_ficha/<int:modelo_id>")
def aba_ficha(modelo_id):
    conn = conectar()

    fichas = conn.execute("""
    SELECT f.*, m.tipo_motor, m.desc_motor
    FROM fichas f
    JOIN motores m ON f.motor_id = m.id
    WHERE f.modelo_id = ?
    """, (modelo_id,)).fetchall()

    modelo = conn.execute("SELECT * FROM modelos WHERE id = ?", (modelo_id,)).fetchone()

    conn.close()

    return render_template("partials/_ficha.html", fichas=fichas, modelo = modelo)

# Abrir Formulário de Ficha de Modelo Específico
@app.route("/admin/ficha/<int:modelo_id>")
def form_ficha(modelo_id):
    return render_template("ficha_form.html", modelo_id=modelo_id)

@app.route("/inserir_avaliacao", methods=["POST"])
def inserir_avaliacao():
    conn = conectar()

    user = request.form["user"]
    mensagem = request.form["mensagem"]
    nota = request.form["nota"]
    modelo_id = request.form["modelo_id"]

    # inserir ficha
    conn.execute("""
    INSERT INTO avaliacoes (user, mensagem, nota, modelo_id) VALUES (?, ?, ?, ?)""", 
    (user, mensagem, nota, modelo_id))

    conn.commit()
    conn.close()

    return redirect("/carros")

# Abrir Formulário de Avaliação
@app.route("/admin/avaliacao/<int:modelo_id>")
def form_avaliacao(modelo_id):

    conn = conectar()
    modelos = conn.execute("""
    SELECT modelos.*, carros.nome AS carro_nome, marcas.nome AS marca_nome
    FROM modelos
    JOIN carros ON modelos.carro_id = carros.id 
    JOIN marcas ON carros.marca_id = marcas.id
    WHERE modelos.id = ?""", (modelo_id,)).fetchone()
    conn.commit()
    conn.close()

    return render_template("aval_form.html", modelo_id=modelo_id, modelos = modelos)