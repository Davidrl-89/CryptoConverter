from flask import render_template, request

from . import app 
from .models import DBManager

RUTA = 'data/balance.db'

@app.route("/")
def inicio():
    db = DBManager(RUTA)
    movimientos = db.consultaSQL("SELECT * FROM movimientos ORDER BY date")
    return render_template("inicio.html", movs = movimientos)


@app.route("/purchase", methods= ["GET", "POST"])
def compra():
    if request.method == "GET":

        return render_template("purchase.html")



@app.route("/status")
def estado():
    return "ver estado"