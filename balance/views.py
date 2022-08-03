from crypt import methods
from . import app 


@app.route("/")
def inicio():
    return "pagina de inicio"


@app.route("/purchase", methods= ["GET", "POST"])
def compra():
    return "crear compras"



@app.route("/status")
def estado():
    return "ver estado"