from flask_wtf import FlaskForm
from flask_wtf.file import FileField,FileRequired
from wtforms import StringField,SubmitField,IntegerField,BooleanField,FloatField
from wtforms.validators import DataRequired, Regexp
from wtforms.widgets import TextArea
from src.models import Configuracion
from werkzeug.security import generate_password_hash,check_password_hash

class Ejecutar(FlaskForm):
    comando = StringField('Comando',validators=[DataRequired()])
    submit = SubmitField('Ejecutar')

class Parar(FlaskForm):
    submit = SubmitField('Parar')

class Seleccionar(FlaskForm):
    upload_file = FileField('Script',validators=[FileRequired()])
    submit = SubmitField('Subir script')

class TrabajandoForm(FlaskForm):
    on = SubmitField('Encender ultima configuracion')
    off = SubmitField('Apagar Indoor')
    on2 = SubmitField(' ')
    off2 = SubmitField(' ')

class IndoorForm(FlaskForm):
    luz = SubmitField('Encender Luz')
    a_luz = SubmitField('Apagar Luz')
    #intractor = SubmitField('Introducir aire')#modificar
    ec_down = SubmitField('Bajar Electroconductividad')
    #a_intractor = SubmitField('Parar de introducir aire')#modificar
    a_ec_down = SubmitField ('Parar de bajar electroconductividad')
    #extractor = SubmitField('Encender extractor')#modificar
    ec_up = SubmitField('Insertar nutrientes')
    #a_extractor = SubmitField('Apagar extractor')#modificar
    a_ec_up = SubmitField('Parar de nutrir')
    riego = SubmitField('Regar')
    a_riego = SubmitField('Parar de Regar')
    humedad = SubmitField('Humedificar')
    a_humedad = SubmitField('Parar de Humedificar')
    #ventilador = SubmitField('Ventilar')#modificar
    intractor_extractor = SubmitField('Ventilar')
    #a_ventilador = SubmitField('Parar de ventilar')#modificar
    a_intractor_extractor = SubmitField('Parar de ventilar')
    ph_up = SubmitField('Subir ph')
    a_ph_up = SubmitField('Parar de subir ph')
    ph_down = SubmitField('Bajar ph')
    a_ph_down = SubmitField('Parar de bajar ph')
    salir = SubmitField('SALIR')


class AutomaticForm(FlaskForm):
    tierra = BooleanField('Cultivo por tierra')
    hidro = BooleanField('Cultivo hidroponico')
    luz = IntegerField('Horas de encendido de la LUZ a partir de ahora',validators=[DataRequired()])
    hum_suelo = BooleanField('Usar sensor de humedad de suelo para regar')
    riego_por_tiempo = BooleanField('Regado por tiempo')
    humedad_suelo = IntegerField('Porcentaje de humedad del suelo', validators=[DataRequired()])
    riego = IntegerField('Cada cuantas horas regar',validators=[DataRequired()])
    cantidad_riego = IntegerField('Cantidad de segundos de riego', validators=[DataRequired()])
    humedad_min = IntegerField('Porcentaje de humedad minima',validators=[DataRequired()])
    humedad_max = IntegerField('Porcentaje de humedad maxina',validators=[DataRequired()])
    temperatura_min = IntegerField('Temperatura minima',validators=[DataRequired()])
    temperatura_max = IntegerField('Temperatura maxima',validators=[DataRequired()])
    ventilador = IntegerField('Cada cuantas horas ventilar', validators=[DataRequired()])
    cantidad_ventilador = IntegerField('Cantidad de minutos de ventilacion', validators=[DataRequired()])
    ph_min = FloatField('Nivel de PH minimo', validators=[DataRequired()])
    ph_max = FloatField('Nivel de PH maximo', validators=[DataRequired()])
    ec_min = FloatField('Total de solidos disueltos minimo (ppm)', validators=[DataRequired()])
    ec_max = FloatField('Total de solidos disueltos maximo (ppm)', validators=[DataRequired()])
    nombre_conf = StringField('Nombre de la configuracion: ', validators=[DataRequired(),Regexp(r'^[\w]+$',0,message='No se pertmiten espacios ni simbolos')])
    submit = SubmitField('Guardar/Actualizar')

    def check_conf(self,name_conf):
        return True if Configuracion.query.filter_by(nombre_conf = name_conf).first() else False

class MensajeAdminForm(FlaskForm):
    asunto = StringField('Asunto:', validators=[DataRequired()])
    mensaje = StringField('Mensaje:', widget=TextArea(), validators=[DataRequired()])
    submit = SubmitField('Enviar')

class TimeLapsForm2(FlaskForm):
    encender = SubmitField('Encender Time Laps')

class TimeLapsForm(FlaskForm):
    nombre_time_laps = StringField('Nombre del archivo Timelaps', validators=[DataRequired(),Regexp(r'^[\w]+$',0,message='No se pertmiten espacios ni simbolos')])
    submit = SubmitField('Apagar, guardar y descargar Timelaps')
