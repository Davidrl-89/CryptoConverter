from flask import flash, render_template, redirect, request, url_for

from . import app
from .models import APIError, DBManager, CriptoModel, Saldo
from .forms import movimientosForm
from datetime import date, datetime
from . import monedas_disponibles


RUTA = 'data/balance.db'


@app.route("/")
def inicio():
    try:
        db = DBManager(RUTA)
        movimientos = db.consultaSQL("SELECT * FROM movimientos ORDER BY date")
        return render_template("inicio.html", movs=movimientos)
    except:
        flash("Error de la BBDD, inténtelo más tarde",
              category="fallo")
        return render_template("inicio.html")


@app.route("/purchase", methods=["GET", "POST"])
def compra():

    if request.method == "GET":
        form = movimientosForm()
        return render_template("purchase.html", form=form)
    else:
        try:
            form = movimientosForm(data=request.form)

            moneda_from = form.moneda_from.data
            moneda_to = form.moneda_to.data
            cantidad_from = form.cantidad_from.data
            cantidad_from = float(round(cantidad_from, 8))

            convertir = CriptoModel(moneda_from, moneda_to)
            PU = convertir.consultar_cambio()
            PU = float(round(PU, 8))
            cantidad_to = cantidad_from * PU
            cantidad_to = float(round(cantidad_to, 8))

            saldo = DBManager(RUTA).calcular_saldo(moneda_from)
            if moneda_from != 'EUR' and saldo < float(cantidad_from):
                flash("No tienes suficientes monedas {} ".format(moneda_from))
                return render_template("purchase.html", form=form)

            
            if form.consultar.data:
                return render_template("purchase.html", form=form, cantidad_to=cantidad_to, PU=PU)

        except APIError as err:
            flash(err)
            return render_template("purchase.html", form=form)

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
                params = (fecha, hora, moneda_from,
                          cantidad_from, moneda_to, cantidad_to)
                resultado = db.consultaConParametros(consulta, params)

                if resultado:
                    flash("Movimiento actualizado correctamente", category="exito")
                    return redirect(url_for("inicio"))

                else:
                    return render_template("purchase.html", form=form, cantidad_to=cantidad_to, errores=["Ha fallado la conexión con las Base de datos"])

            else:
                return render_template("purchase.html", form=form, cantidad_to=cantidad_to, errores=["Ha fallado la validación de datos"])

        else:
            return redirect(url_for("compra"))


@app.route("/status", methods=["GET"])
def estado():
    try:
        db = DBManager(RUTA)
        euros_to = db.consultar_saldo(
            "SELECT sum(cantidad_to) FROM movimientos WHERE moneda_to='EUR'")
        euros_to = euros_to[0]
        euros_from = db.consultar_saldo(
            "SELECT sum(cantidad_from) FROM movimientos WHERE moneda_from='EUR'")
        euros_from = euros_from[0]
        saldo_euros_invertidos = euros_to - euros_from
        saldo_euros_invertidos = round(saldo_euros_invertidos, 6)
        total_euros_ivertidos = euros_from

        cripto_from = db.total_euros_invertidos(
            "SELECT moneda_from, sum(cantidad_from) FROM movimientos GROUP BY moneda_from")
        totales_from = []
        try:

            for valor_from in cripto_from:
                convertir = CriptoModel(valor_from[0], "EUR")
                valor = convertir.consultar_cambio()
                valor = convertir.cambio
                valor = float(valor)
                valor = valor * valor_from[1]
                valor = totales_from.append(valor)
            suma_valor_from = sum(totales_from)

            cripto_to = db.total_euros_invertidos(
                "SELECT moneda_to, sum(cantidad_to) FROM movimientos GROUP BY moneda_to")

            totales_to = []

            for valor_to in cripto_to:
                convertir = CriptoModel(valor_to[0], "EUR")
                valor = convertir.consultar_cambio()
                valor = convertir.cambio
                valor = float(valor)
                valor = valor * valor_to[1]
                valor = totales_to.append(valor)

            suma_valor_to = sum(totales_to)

            inversion_atrapada = suma_valor_to - suma_valor_from
            valor_actual = total_euros_ivertidos + \
                saldo_euros_invertidos + inversion_atrapada
            valor_actual = round(valor_actual, 8)
            return render_template("status.html", euros_to=euros_to, euros_from=euros_from, saldo_euros_invertidos=saldo_euros_invertidos, valoractual=valor_actual)
        except APIError as error:
            return render_template("status.html", errores=[error])
    except:
        flash("Error de conexión de BBDD, inténtelo más tarde",
              category="fallo")
        return render_template("status.html")


@app.route("/saldo")
def saldo():
    try:
        db = DBManager(RUTA)
        saldos = []
        for moneda in monedas_disponibles:
            if moneda != "EUR":
                saldo = db.calcular_saldo(moneda)
                saldos.append(Saldo(moneda, saldo))
        return render_template("saldo.html", saldos=saldos)
    except:
        flash("Error de la BBDD, inténtelo más tarde",
              category="fallo")
        return render_template("saldo.html")
