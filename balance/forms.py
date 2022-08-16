from flask_wtf import FlaskForm
from wtforms import  DateField, FloatField ,HiddenField ,TimeField ,SelectField, SubmitField
from wtforms.validators import DataRequired, NumberRange ,ValidationError




class movimientosForm(FlaskForm):
    id = HiddenField()
    fecha = DateField("Fecha")
    hora = TimeField("Hora")

    moneda_from = SelectField("From: ", choices=[
        ("EUR", "EUR"), ("BTC", "BTC"), ("ETH", "ETH"), ("LUNA", "LUNA"), ("LINK", "LINK")], validators=[DataRequired()])
    moneda_to = SelectField("To: ", choices=[
        ("EUR", "EUR"), ("BTC", "BTC"), ("ETH", "ETH"), ("LUNA", "LUNA"), ("LINK", "LINK")], validators=[DataRequired()])

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
    
