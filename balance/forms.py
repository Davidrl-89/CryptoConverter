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

    cantidad_from = FloatField("Q:  ",validators=[DataRequired(message="La cantidad debe de ser un número positivo y mayor que 0"),
    NumberRange(min=0.00001, max=99999999)])

    consultar = SubmitField("Calcular")

    cantidad_to = FloatField("Q:  ")
    PU = FloatField("PU: ")

    borrar = SubmitField("X")
    aceptar = SubmitField("√")


class EstadoForm(FlaskForm):
    invertido = FloatField("Invertido: ", render_kw={'readonly': True})
    valor_actual = FloatField("Valor actual: ", render_kw={'readonly': True})
    
