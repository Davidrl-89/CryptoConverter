from flask import flash ,render_template, redirect ,request, url_for 

from . import app 
from .models import DBManager, CriptoModel
from .forms import EstadoForm, movimientosForm
from datetime import date, datetime


RUTA = 'data/balance.db'

@app.route("/")
def inicio():
    try:
        db = DBManager(RUTA)
        movimientos = db.consultaSQL("SELECT * FROM movimientos ORDER BY date")
        return render_template("inicio.html", movs = movimientos)
    except:
        flash("Error de la BBDD, inténtelo más tarde",
            category="fallo")
        return render_template("inicio.html")

@app.route("/purchase", methods= ["GET", "POST"])
def compra():

    if request.method == "GET":
        formulario = movimientosForm()
        return render_template("purchase.html", form=formulario)
    else:
        form = movimientosForm(data=request.form)

        moneda_from = form.moneda_from.data
        moneda_to = form.moneda_to.data
        cantidad_from = form.cantidad_from.data
        cantidad_from = float(round(cantidad_from, 8))

        convertir = CriptoModel(moneda_from, moneda_to)
        convertir.consultar_cambio()
        
        PU = convertir.cambio
        PU = float(round(PU, 8))

        cantidad_to = PU * cantidad_from
        cantidad_to = float(round(cantidad_to, 8))

        form.PU = PU
        form.cantidad_to = cantidad_to

      
        if form.consultar.data:
            return render_template("purchase.html", form= form, cantidad_to = cantidad_to, PU = PU)

        if form.aceptar.data:
            if form.validate():
                form = movimientosForm(data=request.form)
                db = DBManager(RUTA)
                consulta = "INSERT INTO movimientos (date, time, moneda_from, cantidad_from, moneda_to, cantidad_to) VALUES (?,?,?,?,?,?)"
                moneda_from = str(form.moneda_from.data)
                moneda_to = str(form.moneda_to.data)
                cantidad_from = float(cantidad_from)
                form.fecha.data = date.today()
                fecha = form.fecha.data
                form.hora.data = datetime.today().strftime("%H:%M:%S")
                hora = form.hora.data
                params = (fecha, hora, moneda_from, cantidad_from, moneda_to, cantidad_to)
                resultado = db.consultaConParametros(consulta, params)

                if resultado:
                    flash("Movimiento actualizado correctamente", category="exito")
                    return redirect(url_for("inicio"))
                
                else:
                    return render_template("purchase.html", form=form, cantidad_to= cantidad_to, errores=["Ha fallado la conexión con las Base de datos"])

            else:
                return render_template("purchase.html", form=form, cantidad_to= cantidad_to, errores=["Ha fallado la validación de datos"] )

        else:
            return redirect(url_for("inicio"))













   
@app.route("/status")
def estado():
    formulario = EstadoForm()
    return render_template("status.html", form=formulario)