from datetime import datetime
from src import db
from sqlalchemy import Column,String,Integer,DateTime,LargeBinary,Text,Binary,Float
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
import uuid



class Users(db.Model,UserMixin):
    __tablename__ = 'users'
    id = Column(Integer,primary_key=True,autoincrement=True)
    username = Column(String(20),unique=True)
    password_hash = Column(String(128))

    def __init__(self,username,password):
        self.username = username
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash,password)

class Configuracion(db.Model):
    __tablename__ = 'configuracion'
    id = Column(Integer,primary_key=True,autoincrement=True)
    tipo_cultivo = Column(String)
    luz = Column(Integer)
    humedad_suelo = Column(Integer)
    riego = Column(Integer)
    cantidad_riego = Column(Integer)
    humedad_min = Column(Integer)
    humedad_max = Column(Integer)
    temperatura_min = Column(Integer)
    temperatura_max = Column(Integer)
    ventilador = Column(Integer)
    cantidad_ventilador = Column(Integer)
    ph_min = Column(Float)
    ph_max = Column(Float)
    ec_min = Column(Float)
    ec_max = Column(Float)
    nombre_conf = Column(String,unique=True)
    inicio = Column(DateTime, default=datetime.now)


    #def __init__(self,luz,humedad_suelo,riego,cantidad_riego,humedad_min,humedad_max,temperatura_min,temperatura_max,nombre_conf,ventilador,cantidad_ventilador,ph_min,ph_max):
    def __init__(self, tipo_cultivo, luz, humedad_suelo, riego, cantidad_riego, humedad_min, humedad_max, temperatura_min, temperatura_max, nombre_conf, ventilador, cantidad_ventilador, ph_min, ph_max, ec_min, ec_max):

        self.tipo_cultivo = tipo_cultivo
        self.luz = luz
        self.humedad_suelo = humedad_suelo
        self.riego = riego
        self.cantidad_riego = cantidad_riego
        self.humedad_min = humedad_min
        self.humedad_max = humedad_max
        self.temperatura_min = temperatura_min
        self.temperatura_max = temperatura_max
        self.nombre_conf = nombre_conf
        self.ventilador = ventilador
        self.cantidad_ventilador = cantidad_ventilador
        self.ph_min = ph_min
        self.ph_max = ph_max
        self.ec_min = ec_min
        self.ec_max = ec_max

class Historial(db.Model):
    __tablename__ = 'historial'
    id = Column(Integer,primary_key=True,autoincrement=True)
    usuario = Column(String)
    nombre_conf = Column(String)
    fecha_hora = Column(DateTime, default=datetime.now)

    def __init__(self,usuario,nombre_conf):
        self.usuario = usuario
        self.nombre_conf = nombre_conf

class Luna(db.Model):
    __tablename__ = 'luna'
    id = Column(Integer,primary_key=True)
    ip = Column(String)
    ciudad = Column(String)
    provincia = Column(String)
    pais = Column(String)
    latitud = Column(String)
    longitud = Column(String)
    hemisferio = Column(String)
    fase = Column(String)
    fecha = Column(String)
    moon_rise = Column(String)
    moon_set = Column(String)
    visibilidad = Column(String)
    estado = Column(String)
    recomendacion = Column(String)
    image = Column(LargeBinary)

    def __init__(self,id,ip,ciudad,provincia,pais,latitud,longitud,hemisferio,fase,fecha,moon_rise,moon_set,visibilidad,estado,recomendacion,image):
        self.id = id
        self.ip = ip
        self.ciudad = ciudad
        self.provincia = provincia
        self.pais = pais
        self.latitud = latitud
        self.longitud = longitud
        self.hemisferio = hemisferio
        self.fase = fase
        self.fecha = fecha
        self.moon_rise = moon_rise
        self.moon_set = moon_set
        self.recomendacion = recomendacion
        self.visibilidad = visibilidad
        self.estado = estado
        self.image = image

class Sensordht22(db.Model):
    __tablename__ = 'sensordht22'
    id = Column(Integer,autoincrement=True,primary_key=True)
    fecha = Column(String)
    hora = Column(String)
    temp = Column(Integer)
    hum = Column(Integer)

    def __init__(self,fecha,hora,temp,hum):
        self.fecha = fecha
        self.hora = hora
        self.temp = temp
        self.hum = hum

class SensorStream(db.Model):
    __tablename__ = 'sensorstream'
    id = Column(Integer,primary_key=True)
    fecha = Column(String)
    hora = Column(String)
    temp = Column(Integer)
    hum = Column(Integer)

    def __init__(self,id,fecha,hora,temp,hum):
        self.id = id
        self.fecha = fecha
        self.hora = hora
        self.temp = temp
        self.hum = hum

class MensajesAdm(db.Model):
    __tablename__ = 'mensajes'
    id = Column(Integer,primary_key=True)
    fecha = Column(String)
    hora = Column(String)
    asunto = Column(String)
    mensaje = Column(String)
    numero_serie_rpi = Column(String)
    ip_rpi = Column(String)
    usuario = Column(String)
    id_mensaje = Column(String)
    respuesta = Column(String)

    def __init__(self,fecha, hora, asunto, mensaje, numero_serie_rpi, ip_rpi, usuario, id_mensaje = None, respuesta = None):
        self.fecha = fecha
        self.asunto = asunto
        self.mensaje = mensaje
        self.numero_serie_rpi = numero_serie_rpi
        self.hora = hora
        self.ip_rpi = ip_rpi
        self.usuario = usuario
        self.id_mensaje = uuid.uuid4().hex if id_mensaje == None else id_mensaje
        self.respuesta = respuesta

class SensorPh(db.Model):
    __tablename__ = 'sensorph'
    id = Column(Integer,autoincrement=True,primary_key=True)
    fecha = Column(String)
    hora = Column(String)
    ph = Column(Float)

    def __init__(self,fecha,hora,ph):
        self.fecha = fecha
        self.hora = hora
        self.ph = ph

class SensorPhStream(db.Model):
    __tablename__ = 'sensorphstream'
    id = Column(Integer,primary_key=True)
    fecha = Column(String)
    hora = Column(String)
    ph = Column(Float)

    def __init__(self,id,fecha,hora,ph):
        self.id = id
        self.fecha = fecha
        self.hora = hora
        self.ph = ph



class SensorPhbigdata(db.Model):
    __tablename__ = 'sensorphbigdata'
    id = Column(Integer,autoincrement=True,primary_key=True)
    fecha = Column(String)
    hora = Column(String)
    ph = Column(Float)

    def __init__(self,fecha,hora,ph):
        self.fecha = fecha
        self.hora = hora
        self.ph = ph



class SensorLuz(db.Model):
    __tablename__ = 'sensorluz'
    id = Column(Integer,autoincrement=True,primary_key=True)
    fecha = Column(String)
    hora = Column(String)
    intensidad_sol = Column(Float)

    def __init__(self,fecha,hora,intensidad_sol):
        self.fecha = fecha
        self.hora = hora
        self.intensidad_sol = intensidad_sol

class SensorLuzStream(db.Model):
    __tablename__ = 'sensorluzstream'
    id = Column(Integer,primary_key=True)
    fecha = Column(String)
    hora = Column(String)
    luz = Column(Integer)
    sol = Column(Integer)

    def __init__(self,id,fecha,hora,luz,sol):
        self.id = id
        self.fecha = fecha
        self.hora = hora
        self.luz = luz
        self.sol = sol



class SensorHumSuelo(db.Model):
    __tablename__ = 'sensorhumsuelo'
    id = Column(Integer,autoincrement=True,primary_key=True)
    fecha = Column(String)
    hora = Column(String)
    hum_suelo = Column(Float)

    def __init__(self,fecha,hora,hum_suelo):
        self.fecha = fecha
        self.hora = hora
        self.hum_suelo = hum_suelo

class SensorHumSueloStream(db.Model):
    __tablename__ = 'sensorhumsuelostream'
    id = Column(Integer,primary_key=True)
    fecha = Column(String)
    hora = Column(String)
    hum_suelo = Column(Float)

    def __init__(self,id,fecha,hora,hum_suelo):
        self.id = id
        self.fecha = fecha
        self.hora = hora
        self.hum_suelo = hum_suelo


class SensorEc(db.Model):
    __tablename__ = 'sensorec'
    id = Column(Integer,autoincrement=True,primary_key=True)
    fecha = Column(String)
    hora = Column(String)
    ec = Column(Float)

    def __init__(self,fecha,hora,ec):
        self.fecha = fecha
        self.hora = hora
        self.ec = ec

class SensorEcStream(db.Model):
    __tablename__ = 'sensorecstream'
    id = Column(Integer,primary_key=True)
    fecha = Column(String)
    hora = Column(String)
    ec = Column(Float)

    def __init__(self,id,fecha,hora,ec):
        self.id = id
        self.fecha = fecha
        self.hora = hora
        self.ec = ec
