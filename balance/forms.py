from flask_wtf import FlaskForm
from wtforms import  FloatField ,HiddenField , SelectField, SubmitField
from wtforms.validators import DataRequired, NumberRange ,ValidationError


def validar_moneda(form, field):
    if field.data == form.moneda_from.data:
        raise ValidationError("Debe elegir distintos tipos de monedas")



class movimientosForm(FlaskForm):
    id = HiddenField()
    fecha = HiddenField("Fecha")
    hora = HiddenField("Hora")

    moneda_from = SelectField("From: ", choices=[
        ("EUR", "EUR"), ("BTC", "BTC"), ("ETH", "ETH"), ("LUNA", "LUNA"), ("LINK", "LINK")], validators=[DataRequired()])
    moneda_to = SelectField("To: ", choices=[
        ("EUR", "EUR"), ("BTC", "BTC"), ("ETH", "ETH"), ("LUNA", "LUNA"), ("LINK", "LINK")], validators=[DataRequired(), validar_moneda])

    cantidad_from = FloatField("Cantidad",validators=[DataRequired(message="La cantidad debe de ser un número positivo y mayor que 0"),
    NumberRange(min=0.00001, max=99999999)] ,places=8)

    consultar = SubmitField("Consultar")

    cantidad_to = FloatField("Cantidad2")
    PU = FloatField("Precio unitario: ")

    borrar = SubmitField("Borrar")
    aceptar = SubmitField("Guardar")
