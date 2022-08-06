from flask_wtf import FlaskForm
from wtforms import DecimalField ,HiddenField , SelectField, SubmitField

'''
ME FALTA PONER DATOS REQUERIDOS
'''

class movimientosForm(FlaskForm):
    id = HiddenField()
    fecha = HiddenField("Fecha")
    moneda1 = SelectField("From: ", choices=[
        ("EUR", "EUR"), ("BTC", "BTC"), ("ETH", "ETH"), ("LUNA", "LUNA"), ("LINK", "LINK")])
    moneda2 = SelectField("To: ", choices=[
        ("EUR", "EUR"), ("BTC", "BTC"), ("ETH", "ETH"), ("LUNA", "LUNA"), ("LINK", "LINK")])
    cantidad = DecimalField("Cantidad", places=8)
    consultar = SubmitField("Consultar")
    cantidad2 = DecimalField("Cantidad2")
    PU = DecimalField("Precio unitario: ")
    borrar = SubmitField("Borrar")
    aceptar = SubmitField("Guardar")
