from flask import Blueprint,render_template,url_for,redirect,request,session,flash, send_file, send_from_directory
from flask_login import login_required
from werkzeug.utils import secure_filename
from src import app,db
from src.core.forms import Ejecutar,Seleccionar,Parar,IndoorForm,AutomaticForm, TrabajandoForm,MensajeAdminForm,TimeLapsForm,TimeLapsForm2
import paramiko
import time
from time import sleep
from datetime import datetime
import os
from src.comando import ParamikoComando
from src.models import Configuracion, Historial, Luna, Sensordht22,SensorStream, MensajesAdm, SensorPhStream, SensorHumSueloStream, SensorEcStream
import base64
from src.core.conexion import Conexion2

##################################
############INSTANCIAS############
##################################
luz = ParamikoComando()
#luz.conectar()

humedad = ParamikoComando()
#humedad.conectar()

riego = ParamikoComando()
#riego.conectar()

#intractor = ParamikoComando()#modificar
ec_down = ParamikoComando()

#extractor = ParamikoComando()#modificar
ec_up = ParamikoComando()


#ventilador = ParamikoComando()#modificar
intractor_extractor = ParamikoComando()

ph_down = ParamikoComando()

ph_up = ParamikoComando()

#servicios = [luz,humedad,riego,intractor,extractor,ventilador,ph_down,ph_up]#modificar
servicios = [luz,humedad,riego,ec_down,ec_up,intractor_extractor,ph_down,ph_up]#modificar

#################################
#################################
###########GLOBALS###############
ban_luz = False
#ban_int = False#modificar ban_ec_down
ban_ec_down = False
ban_hum = False
ban_rie = False
#ban_ext = False#modificar ban_ec_up
ban_ec_up = False
#ban_ven = False#modificar ban_int_ext
ban_int_ext = False
ban_ph_up = False
ban_ph_down = False
TRABAJANDO = False
INSTANCIAS = True
BANDERAS = []
HUMEDAD = ''
TEMPERATURA = ''
PH = 0
SUELO = 0
EC = 0
TIPO_CULTIVO = ''
#TEMP_AGUA = ''

##################################
core = Blueprint('core',__name__)

def guardar_en_historial(usuario,nombre):
    historial = Historial(usuario=usuario, nombre_conf=nombre)
    db.session.add(historial)
    db.session.commit()
    return True

def encender_sensorDHT22():
    sensor = ParamikoComando()
    sensor.conectar()
    try:
        comando = 'pigpiod_py.py'
        sensor.ejecutarcomando(comando, False)
    except:
        pass
    comando = 'datosdh22.py'
    if sensor.pid(comando) != []:
        print('El sensor DHT22 ya esta encendido')
    else:
        sensor.ejecutarcomando(comando, False)
        print('Sensor DHT22 encendido')
        #sensor.client.close()
        return True

def matar_instancias():
    global INSTANCIAS
    try:
        for s in servicios:
            s.client.close()
        INSTANCIAS = False
    except:
        pass

def comprobar_automatic():
    global TRABAJANDO
    try:
        automatic = ParamikoComando()
        automatic.conectar()
        comando = 'automatic.py'
        if automatic.pid(comando) != []:
            TRABAJANDO = True
            encender_sensorDHT22()
            ultima_conf = Historial.query.order_by(Historial.id.desc()).first()
            session['nombre_conf'] = ultima_conf.nombre_conf
            confi = Configuracion.query.filter_by(nombre_conf=session['nombre_conf']).first()
            session['tipo_cultivo'] = confi.tipo_cultivo
            session['luz'] = confi.luz
            session['humedad_suelo'] = confi.humedad_suelo
            session['riego'] = confi.riego
            session['cantidad_riego'] = confi.cantidad_riego
            session['humedad_min'] = confi.humedad_min
            session['humedad_max'] = confi.humedad_max
            session['temperatura_min'] = confi.temperatura_min
            session['temperatura_max'] = confi.temperatura_max
            session['ventilador'] = confi.ventilador
            session['cantidad_ventilador'] = confi.cantidad_ventilador
            session['ph_min'] = confi.ph_min
            session['ph_max'] = confi.ph_max
            session['ec_min'] = confi.ec_min
            session['ec_max'] = confi.ec_max
            session['trabajando'] = True
            session['inicio'] = confi.inicio

            return True
        else:
            TRABAJANDO = False
            session['trabajando'] = False
        automatic.client.close()
    except:
        pass
def comprobar_camara():
    camara = ParamikoComando()
    camara.conectar()
    comando = 'camara.py'
    if camara.pid(comando) != []:
        session['camara'] = 1
    else:
        session['camara'] = 0

def matar_camara():
    camara = ParamikoComando()
    camara.conectar()
    comando = 'camara.py'
    try:
        ####MATANDO CAMARA.PY##################
        print('matando camara.py')
        for pid in camara.pid(comando):
            pid_a_matar = pid.strip('\n')
            camara.matarsig(pid_a_matar)
        session['camara'] = 0
    except:
        pass
    camara.client.close()
    print('Camara apagada')


def comprobar_timelaps():
    timelaps = ParamikoComando()
    timelaps.conectar()
    comando = 'fotos.py'
    if timelaps.pid(comando) != []:
        session['timelaps'] = 1
        return True
    else:
        session['timelaps'] = 0
        return False

def matar_timelaps():
    timelaps = ParamikoComando()
    timelaps.conectar()
    comando = 'fotos.py'
    try:
        ####MATANDO FOTOS.PY##################
        print('matando fotos.py')
        for pid in timelaps.pid(comando):
            pid_a_matar = pid.strip('\n')
            timelaps.matarsig(pid_a_matar)
        session['timelaps'] = 0
    except:
        pass
    timelaps.client.close()
    print('Timelaps apagado')


def comprobar_ecosystem():
    ecoluz = ParamikoComando()
    ecoluz.conectar()
    comando = 'ecosystem.py'
    if ecoluz.pid(comando) != []:
        session['ecosystem'] = 1
    else:
        session['ecosystem'] = 0

def matar_ecosystem():
    ecoluz = ParamikoComando()
    ecoluz.conectar()
    comando = 'ecosystem.py'
    try:
        ####MATANDO ECOSYSTEM.PY##################
        print('matando ecosystem.py')
        for pid in ecoluz.pid(comando):
            pid_a_matar = pid.strip('\n')
            ecoluz.matarsig(pid_a_matar)
        session['ecosystem'] = 0
    except:
        pass
    ecoluz.client.close()
    print('Ecosystem apagado')


def matar_automatic():
    automatic = ParamikoComando()
    automatic.conectar()

    try:
        ####MATANDO AUTIMATIC.PY##################
        print('matando automatic.py')
        comando = 'automatic.py'
        for pid in automatic.pid(comando):
            pid_a_matar = pid.strip('\n')
            automatic.matar(pid_a_matar)
    except:
        pass
    automatic.client.close()


def matar_datosdh22():
    automatic = ParamikoComando()
    automatic.conectar()
    try:
        ####MATANDO SENSOR##########
        print('matando datosdh22.py')
        comando = 'datosdh22.py'
        for pid in automatic.pid(comando):
            pid_a_matar = pid.strip('\n')
            automatic.matar(pid_a_matar)
    except:
        pass
    automatic.client.close()

def liberar_gpios():
    automatic = ParamikoComando()
    automatic.conectar()
    comando = 'liberar_gpios.py'
    stdin, stdout, stderr = automatic.ejecutarcomando(comando, False)  #
    automatic.client.close()

def ejecutar_automatic(nombre_conf):
    global TRABAJANDO
    automatic = ParamikoComando()
    automatic.conectar()
    comando = 'automatic.py ' + nombre_conf
    guardar_en_historial(session['username'], nombre_conf)
    stdin, stdout, stderr = automatic.ejecutarcomando(comando, False)
    TRABAJANDO = True
    session['nombre_conf'] = nombre_conf
    session['inicio'] = datetime.now()
    Configuracion.query.filter_by(nombre_conf=nombre_conf).update(
        {Configuracion.inicio: session['inicio']}, synchronize_session=False)
    db.session.commit()
    #prueba = stdout.readlines()
    #print(prueba)

@login_required
@core.route('/home/<string:user>', methods=['GET','POST'])
def home(user):
    global TRABAJANDO, INSTANCIAS, HUMEDAD, TEMPERATURA, PH, SUELO, EC #agregar EC en este endpoint y en los templates renderizados
    #estado_suelo = 'Seco' if SUELO > 0.4 else 'Humedo'

    estado_suelo = SUELO
    electroconductividad = EC
    ultima_c = Historial.query.order_by(Historial.id.desc()).first()
    session['nombre_conf'] = ultima_c.nombre_conf
    confi = Configuracion.query.filter_by(nombre_conf=session['nombre_conf']).first()
    tipo_cultivo = confi.tipo_cultivo
    if tipo_cultivo == 'hidroponico':
        estado_suelo = 100
    comprobar_automatic()
    comprobar_ecosystem()
    comprobar_timelaps()
    #comprobar_camara()

    form = TrabajandoForm()
    if form.validate_on_submit():
        if form.on.data == True:# or form.on2.data == True:
            form.on.data = False
            #form.on2.data = False
            try:
                ultima_conf = Historial.query.order_by(Historial.id.desc()).first()
                nombre = ultima_conf.nombre_conf

                return redirect(url_for('.abrir',nombre=nombre))
            except:
                pass

        if form.off.data == True:# or form.off2.data == True:
            print('Indoor Apagado')
            form.off.data = False
            #form.off2.data = False
            TRABAJANDO = False
            session['trabajando'] = False

            matar_instancias()
            liberar_gpios()
            matar_automatic()
            matar_datosdh22()
            matar_ecosystem()
            matar_timelaps()
    return render_template('home.html',user=user, TRABAJANDO=TRABAJANDO,form=form,humedad=HUMEDAD,temperatura=TEMPERATURA, ph=PH, suelo=estado_suelo, ec=electroconductividad)

@login_required
@core.route('/ejecutar/comando', methods=['POST','GET'])
def comando():

    form = Ejecutar()
    if form.validate_on_submit():
        comando = form.comando.data
        proceso = ParamikoComando()
        proceso.conectar()
        stdin,stdout,stderr = proceso.ejecutarcomando(comando,True)

        proceso.client.close()
        return render_template('stdout.html',form=form,stdin=stdin,stdout=stdout,stderr=stderr,comando=comando)

    return render_template('comando.html',form=form)


@login_required
@core.route('/terminal', methods=['POST','GET'])
def terminal():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    HOST = 'localhost'
    USERNAME = 'xxx'
    PASSWORD = '12345'
    client.connect(HOST, username=USERNAME, password=PASSWORD)
    transport = client.get_transport()
    ssh_session = transport.open_session()
    ssh_session.get_pty()
    shell = ssh_session.invoke_shell()
    print(shell)

    return render_template('terminal.html',shell=shell)


@login_required
@core.route('/subir_archivo', methods=['POST','GET'])
def upload():
    form = Seleccionar()
    if form.validate_on_submit():
        print('copiando')
        basedir = os.path.abspath(os.path.dirname(__file__))
        file = form.upload_file.data
        filename = secure_filename(file.filename)
        file.save(basedir+'/uploads/'+ filename)
        #client.connect(HOST, username=USERNAME, password=PASSWORD)
        proceso = ParamikoComando()
        proceso.conectar()
        ftp_client = proceso.client.open_sftp()
        #ftp_client.put(basedir+'/uploads/'+filename, '/home/mrthc/paramiko/'+filename)
        ftp_client.put(basedir+'/uploads/'+filename, '/home/pi/indoor/'+filename)
        ftp_client.close()
        proceso.client.close()

    return render_template('subir_archivo.html',form=form)



@login_required
#@core.route('/parar/<string:comando>',methods=['POST','GET'])
@core.route('/parar',methods=['POST','GET'])
def parar():
    #print(comando +'este es el comando pasado')
    #proceso = ParamikoComando()
    #proceso.conectar()

    #li = " | sudo -S ps aux|grep" + comando + "|grep -v grep |awk '{print $2}'"

    #stdin, stdout, stderr = ParamikoComando.client.exec_command('echo  ' + ParamikoComando.PASSWORD + li)
    #print(comando)
    ParamikoComando().client.close()

    return render_template('home.html')
#############################################################################

@login_required
@core.route('/indoor',methods=['POST','GET'])
def indoor():
    #global ban_hum,ban_int,ban_rie,ban_luz,ban_ext,ban_ven,ban_ph_down,ban_ph_up,t,TRABAJANDO, INSTANCIAS, BANDERAS
    global ban_hum,ban_ec_down,ban_rie,ban_luz,ban_ec_up,ban_int_ext,ban_ph_down,ban_ph_up,t,TRABAJANDO, INSTANCIAS, BANDERAS
    comandos = ['apagar_proceso1.py','apagar_proceso2.py','apagar_proceso3.py','apagar_proceso4.py','apagar_proceso5.py','apagar_proceso6.py','apagar_proceso7.py','apagar_proceso8.py']
    form = IndoorForm()

    if form.salir.data == True and BANDERAS == []:
        return redirect(url_for('.home', user=session['username']))

    if form.validate_on_submit() and form.salir.data == False:
        TRABAJANDO = False

        if comprobar_automatic():
            liberar_gpios()
            matar_automatic()
            matar_datosdh22()
            matar_timelaps()
            matar_ecosystem()

            sleep(1)

        if form.luz.data == True:
            luz.conectar()
            print('Luz encendida')
            comando = 'proceso1.py'
            stdin, stdout, stderr = luz.ejecutarcomando(comando,True)
            form.luz.data = False
            ban_luz = True
            BANDERAS.append(1)
        if form.a_luz.data == True:
            print('luz apagada')

            comando = comandos[0]
            stdin, stdout, stderr = luz.ejecutarcomando(comando, False)

            luz.client.close()
            form.a_luz.data = False
            luz.conectar()
            ban_luz = False
            BANDERAS.append(1)
########cambiar form.intractor.data por form.ec_down.data
        if form.ec_down.data == True:
            ec_down.conectar()
            print('ec down encendido')
            comando = 'proceso2.py'#editar proceso2.py
            stdin, stdout, stderr = ec_down.ejecutarcomando(comando,True)
            form.ec_down.data = False
            ban_ec_down = True
            BANDERAS.append(1)
        if form.a_ec_down.data == True:
            print('ec down apagado')

            comando = comandos[1]
            stdin, stdout, stderr = ec_down.ejecutarcomando(comando, False)

            ec_down.client.close()
            form.a_ec_down.data = False
            ec_down.conectar()
            ban_ec_down = False
            BANDERAS.append(1)
#####################################################################
        if form.humedad.data == True:
            humedad.conectar()
            print('Humedificador encendido')
            comando = 'proceso3.py'
            stdin, stdout, stderr = humedad.ejecutarcomando(comando,True)
            form.humedad.data = False
            ban_hum = True
            BANDERAS.append(1)
        if form.a_humedad.data == True:
            print('Humedificador apagado')

            comando = comandos[2]
            stdin, stdout, stderr = humedad.ejecutarcomando(comando, False)

            humedad.client.close()
            form.a_humedad.data = False
            humedad.conectar()
            ban_hum = False
            BANDERAS.append(1)
        if form.riego.data == True:
            riego.conectar()
            print('Riego encendido')
            comando = 'proceso4.py'
            stdin, stdout, stderr = riego.ejecutarcomando(comando,True)
            form.riego.data = False
            ban_rie = True
            BANDERAS.append(1)
        if form.a_riego.data == True:
            print('Riego apagado')

            comando = comandos[3]
            stdin, stdout, stderr = riego.ejecutarcomando(comando, False)

            riego.client.close()
            form.a_riego.data = False
            riego.conectar()
            ban_rie = False
            BANDERAS.append(1)
############CAMBIAR form.extractor.data por form.ec_up.data#############
        if form.ec_up.data == True:
            ec_up.conectar()
            print('ec up encendido')
            comando = 'proceso5.py'#editar proceso5.py
            stdin, stdout, stderr = ec_up.ejecutarcomando(comando,True)
            form.ec_up.data = False
            ban_ec_up = True
            BANDERAS.append(1)
        if form.a_ec_up.data == True:
            print('ec up apagado')

            comando = comandos[4]
            stdin, stdout, stderr = ec_up.ejecutarcomando(comando, False)

            ec_up.client.close()
            form.a_ec_up.data = False
            ec_up.conectar()
            ban_ec_up = False
            BANDERAS.append(1)
#####################CAMBIAR form.ventilador.data form.intractor_extractor.data ########################
        if form.intractor_extractor.data == True:
            intractor_extractor.conectar()
            print('Intractor y extractor encendidos')
            comando = 'proceso6.py'
            stdin, stdout, stderr = intractor_extractor.ejecutarcomando(comando,True)
            form.intractor_extractor.data = False
            ban_int_ext = True
            BANDERAS.append(1)
        if form.a_intractor_extractor.data == True:
            print('Intractor y extractor apagados')

            comando = comandos[5]
            stdin, stdout, stderr = intractor_extractor.ejecutarcomando(comando, False)

            intractor_extractor.client.close()
            form.a_intractor_extractor.data = False
            intractor_extractor.conectar()
            ban_int_ext = False
            BANDERAS.append(1)

        if form.ph_up.data == True:
            ph_up.conectar()
            print('Subiendo ph')
            comando = 'proceso7.py'
            stdin, stdout, stderr = ph_up.ejecutarcomando(comando,True)
            form.ph_up.data = False
            ban_ph_up = True
            BANDERAS.append(1)
        if form.a_ph_up.data == True:
            print('Subidor de ph apagado')

            comando = comandos[6]
            stdin, stdout, stderr = ph_up.ejecutarcomando(comando, False)

            ph_up.client.close()
            form.a_ph_up.data = False
            ph_up.conectar()
            ban_ph_up = False
            BANDERAS.append(1)
####################################################
        if form.ph_down.data == True:
            ph_down.conectar()
            print('Bajando ph')
            comando = 'proceso8.py' #editar proceso8.py
            stdin, stdout, stderr = ph_down.ejecutarcomando(comando,True)
            form.ph_down.data = False
            ban_ph_down = True
            BANDERAS.append(1)
        if form.a_ph_down.data == True:
            print('Bajador de ph apagado')

            comando = comandos[7]
            stdin, stdout, stderr = ph_down.ejecutarcomando(comando, False)

            ph_down.client.close()
            form.a_ph_down.data = False
            ph_down.conectar()
            ban_ph_down = False
            BANDERAS.append(1)
##############################################################################################
    if form.salir.data == True and BANDERAS == []:

        return redirect(url_for('.home', user=session['username']))

    if form.salir.data == True and BANDERAS != []:
        print(BANDERAS)
        BANDERAS = []
        a = 0
        while a <= 7:
            for s in servicios:
                print(a)
                try:
                  #  s.conectar()
                    s.ejecutarcomando(comandos[a], False)
                  #  s.client.close()
                    sleep(0.2)
                    a += 1
                except:
                    print(a)
                    print('que ondaaaaa+??')
                    pass
        try:

            for s in servicios:
                s.client.close()
            INSTANCIAS = False
            ban_luz = False
            #ban_int = False #cambiar por el de abajo
            ban_ec_down = False
            ban_hum = False
            ban_rie = False
            #ban_ext = False #cambiar por el de abajo
            ban_ec_up = False
            #ban_ven = False #cambiar por el de abajo
            ban_int_ext = False
            ban_ph_down =False
            ban_ph_up = False
            liberar_gpios()
        except:
            pass
        finally:
            return redirect(url_for('.home',user=session['username']))
########cambiar aca las variables que se van al renderizado de template
    return render_template('indoor.html',form = form, ban_luz = ban_luz, ban_rie = ban_rie, ban_ec_down = ban_ec_down, ban_hum = ban_hum, ban_ec_up = ban_ec_up, ban_int_ext = ban_int_ext, ban_ph_down = ban_ph_down, ban_ph_up = ban_ph_up)


@login_required
@core.route('/cargar', methods=['GET','POST'])
def cargar():
    nconf = Configuracion.query.filter(Configuracion.nombre_conf != None).all()
    return render_template('nombreconf.html', nconf = nconf)


@login_required
@core.route('/abrir/<string:nombre>', methods=['GET','POST'])
def abrir(nombre):
    global TRABAJANDO, INSTANCIAS
    matar_instancias()
    liberar_gpios()
    sleep(3)
    matar_automatic()
    matar_datosdh22()
    matar_timelaps()
    matar_ecosystem()
    print('ESTE ES EL NOMBRE DEL ARGUMENTO EN LA POSICION 1 DEL ARCHIVO AUTOMATIC.PY '+nombre)
    encender_sensorDHT22()
    ejecutar_automatic(nombre_conf=nombre)

    return redirect(url_for('.home', user=session['username']))


@login_required
@core.route('/automatico', methods=['GET','POST'])
def automatico():
    global TRABAJANDO, INSTANCIAS
    form = AutomaticForm()
    if form.validate_on_submit():
        matar_instancias()
        liberar_gpios()
        matar_automatic()
        matar_datosdh22()
        matar_timelaps()
        matar_ecosystem()
        tipo_cultivo = ''
        nombre = form.nombre_conf.data
        ph_min = float(form.ph_min.data)
        ph_max = float(form.ph_max.data)
        ec_min = float(form.ec_min.data)
        ec_max = float(form.ec_max.data)
        print('aca va el de humedad del suelo')
        print(form.hum_suelo.data)
        if form.tierra.data == True:
            tipo_cultivo = 'tierra'
        if form.hidro.data == True:
            tipo_cultivo = 'hidroponico'
            form.riego.data = 0
            form.cantidad_riego.data = 0
            form.humedad_suelo.data = 0
#####cambiar variales al los renderizados
        if form.check_conf(nombre):
            flash('Ya existe una configuracion con ese nombre, desea sobreescribirla?','warning')
            return render_template('borrar_actualizar.html', tipo_cultivo=tipo_cultivo, luz=form.luz.data, humedad_suelo=form.humedad_suelo.data,riego=form.riego.data,cantidad_riego=form.cantidad_riego.data, humedad_min=form.humedad_min.data,humedad_max=form.humedad_max.data,temperatura_min=form.temperatura_min.data,temperatura_max=form.temperatura_max.data,nombre_conf = form.nombre_conf.data,ventilador = form.ventilador.data, cantidad_ventilador = form.cantidad_ventilador.data, ph_min = ph_min, ph_max = ph_max, ec_min = ec_min, ec_max = ec_max)
        else:
            if form.hum_suelo.data == True:
                form.riego.data = 0
                form.cantidad_riego.data = 0
            else:
                form.humedad_suelo.data = 0
            configuracion = Configuracion(
                tipo_cultivo=tipo_cultivo, luz=form.luz.data, humedad_suelo=form.humedad_suelo.data,riego=form.riego.data,cantidad_riego=form.cantidad_riego.data, humedad_min=form.humedad_min.data,humedad_max=form.humedad_max.data,
                temperatura_min=form.temperatura_min.data,temperatura_max=form.temperatura_max.data, nombre_conf = form.nombre_conf.data, ventilador = form.ventilador.data, cantidad_ventilador = form.cantidad_ventilador.data,
                ph_min = ph_min, ph_max = ph_max, ec_min = ec_min, ec_max = ec_max
            )
            db.session.add(configuracion)
            db.session.commit()
            encender_sensorDHT22()
            ejecutar_automatic(nombre_conf=nombre)

            return redirect(url_for('.home',user = session['username']))
    return render_template('automatico.html',form = form )

#########aca en la actiualizacion tambien haceer los cambios pertinentes
@login_required
@core.route('/update/<string:nombre_conf>/<string:tipo_cultivo>/<int:luz>/<int:temperatura_min>/<int:temperatura_max>/<int:riego>/<int:cantidad_riego>/<int:humedad_min>/<int:humedad_max>/<int:ventilador>/<int:cantidad_ventilador>/<float:ph_min>/<float:ph_max>/<int:humedad_suelo>/<float:ec_min>/<float:ec_max>', methods=['GET','POST'])
#@core.route('/update/<string:nombre_conf>/<int:luz>/<int:temperatura_min>/<int:temperatura_max>/<int:riego>/<int:cantidad_riego>/<int:humedad_min>/<int:humedad_max>/<int:ventilador>/<int:cantidad_ventilador>/<float:ph_min>/<float:ph_max>/<int:humedad_suelo>', methods=['GET','POST'])
#def update(nombre_conf,luz,temperatura_min,temperatura_max,riego,cantidad_riego,humedad_min,humedad_max,ventilador,cantidad_ventilador,ph_min,ph_max,humedad_suelo):
def update(nombre_conf, tipo_cultivo, luz, temperatura_min, temperatura_max, riego, cantidad_riego, humedad_min, humedad_max, ventilador, cantidad_ventilador, ph_min, ph_max, humedad_suelo, ec_min, ec_max):

    global TRABAJANDO, INSTANCIAS

    matar_instancias()
    liberar_gpios()
    matar_automatic()
    matar_datosdh22()
    matar_timelaps()
    matar_ecosystem()
    if humedad_suelo != 0 and humedad_suelo != 1:
        riego = 0
        cantidad_riego = 0
    if humedad_suelo == 1:
        humedad_suelo = 0
    if tipo_cultivo == 'hidroponico':
        riego = 0
        cantidad_riego = 0
        humedad_suelo = 0

    session['inicio'] = datetime.now()
######aca abajo hay que  agregar al final Configuracion.ec_min: ec_min, Configuracion.ec_max: ec_max
    Configuracion.query.filter_by(nombre_conf=nombre_conf).update(
        {Configuracion.tipo_cultivo: tipo_cultivo, Configuracion.luz: luz, Configuracion.humedad_suelo: humedad_suelo, Configuracion.riego: riego, Configuracion.cantidad_riego: cantidad_riego ,Configuracion.temperatura_min: temperatura_min, Configuracion.temperatura_max: temperatura_max, Configuracion.humedad_min: humedad_min, Configuracion.humedad_max: humedad_max, Configuracion.ventilador: ventilador, Configuracion.cantidad_ventilador:cantidad_ventilador, Configuracion.ph_min:ph_min, Configuracion.ph_max:ph_max, Configuracion.inicio:session['inicio'], Configuracion.ec_min:ec_min, Configuracion.ec_max:ec_max}, synchronize_session=False)
    db.session.commit()
    encender_sensorDHT22()
    ejecutar_automatic(nombre_conf=nombre_conf)

    flash(f'Configuracion {nombre_conf}, actualizada satisfactoriamente y ejecutandose.','success')

    return redirect(url_for('.home',user = session['username']))


@login_required
@core.route('/delete/<string:nombre_conf>', methods=['GET','POST'])
def delete(nombre_conf):
    conf_del = Configuracion.query.filter(Configuracion.nombre_conf == nombre_conf).first()
    db.session.delete(conf_del)
    db.session.commit()

    flash(f'Configuracion {nombre_conf} borrada satisfactoriamente, realice otra configuracion porfavor', 'success')

    return redirect(url_for('.automatico'))


@login_required
@core.route('/luna')
def luna():
    proceso = ParamikoComando()
    proceso.conectar()
    comando = 'luna2.py'
    stdin, stdout, stderr = proceso.ejecutarcomando(comando, False)
    print('comando '+comando+' ejecutado')
    luna_hoy = Luna.query.filter_by(id=1).first()
    luna_fases = Luna.query.order_by(Luna.id.asc()).all()
    dia = str(datetime.today().day)
    mes = str(datetime.today().month)
    anio = str(datetime.today().year)
    print(dia+'/'+mes+'/'+anio)
    img_dia1 = Luna.query.filter_by(id=1).first()
    img_dia2 = Luna.query.filter_by(id=2).first()
    img_dia3 = Luna.query.filter_by(id=3).first()
    img_dia4 = Luna.query.filter_by(id=4).first()
    img_dia5 = Luna.query.filter_by(id=5).first()
    img_dia6 = Luna.query.filter_by(id=6).first()
    img_dia7 = Luna.query.filter_by(id=7).first()
    dia1 = base64.b64encode(img_dia1.image).decode('ascii')
    dia2 = base64.b64encode(img_dia2.image).decode('ascii')
    dia3 = base64.b64encode(img_dia3.image).decode('ascii')
    dia4 = base64.b64encode(img_dia4.image).decode('ascii')
    dia5 = base64.b64encode(img_dia5.image).decode('ascii')
    dia6 = base64.b64encode(img_dia6.image).decode('ascii')
    dia7 = base64.b64encode(img_dia7.image).decode('ascii')

    return render_template('luna.html',luna_hoy = luna_hoy, luna_fases = luna_fases, dia =dia, mes = mes, anio = anio,
                           dia1 = dia1, dia2 = dia2, dia3 = dia3, dia4 = dia4, dia5 = dia5, dia6 = dia6, dia7 = dia7)


@login_required
@core.route('/sensor')
def sensor():
    global HUMEDAD,TEMPERATURA,PH,SUELO,EC
    consulta = SensorStream.query.order_by(SensorStream.id.desc()).first()
    HUMEDAD = consulta.hum
    TEMPERATURA = consulta.temp
    consulta_ph = SensorPhStream.query.order_by(SensorPhStream.id.desc()).first()
    PH = consulta_ph.ph
    consulta_suelo = SensorHumSueloStream.query.order_by(SensorHumSueloStream.id.desc()).first()
    SUELO = consulta_suelo.hum_suelo
    consulta_ec = SensorEcStream.query.order_by(SensorEcStream.id.desc()).first()
    EC = consulta_ec.ec

    return redirect(url_for('.home',user = session['username']))

@login_required
@core.route('/ecosystem/<int:eco>')
def ecosystem(eco):
    ecoluz = ParamikoComando()
    ecoluz.conectar()
    comando = 'ecosystem.py'
    session['ecosystem'] = eco
    if session['ecosystem'] == 0:
        matar_ecosystem()
    else:
        ecoluz.ejecutarcomando(comando, False)
        print('Ecosystem encendido')

    return redirect(url_for('.home', user = session['username']))

@login_required
@core.route('/camara/<int:cam>')
def camara(cam):
    camara = ParamikoComando()
    camara.conectar()
    opcion  = 'on' if cam==1 else 'off'
    comando = 'camara.py '+opcion
    camara.ejecutarcomando(comando, False)
    session['camara'] = cam
    if session['camara'] == 0:
        matar_camara()

        print('camara apagada')
    else:
        session['camara'] = 1
        print('camara encendida')

    return redirect(url_for('.home',user = session['username']))

@login_required
@core.route('/timelaps', methods=['GET','POST'])
def timelaps():
    form = TimeLapsForm()  # (sale opcion de ponerle nombre y guardarlo)
    form2 = TimeLapsForm2()  # sale opcion de encender
    comprobar_timelaps()
    if comprobar_timelaps():
        if form.validate_on_submit():
            matar_timelaps()
            compositor = ParamikoComando()
            compositor.conectar()
            comando = 'timelaps.py '+ form.nombre_time_laps.data
            stdin, stdout, stderr = compositor.ejecutarcomando(comando, False)
            exit_status = stdout.channel.recv_exit_status()
            if exit_status == 0:
                print(f'Timelaps Guardado con el nombre de: {form.nombre_time_laps.data}.mp4')
                session['timelaps'] = 0
                compositor.client.close()
                archivo = str(form.nombre_time_laps.data)
                link = 'static/'+archivo+'.zip'
                return render_template('descarga.html', link=link)
        return render_template('timelaps.html', form=form, form2=form2)

    else:
        if form2.validate_on_submit():
            flash('Este proceso puede tardar algunos minutos, pronto saldra la opcion de descarga', 'info')
            fotos = ParamikoComando()
            fotos.conectar()
            comando = 'fotos.py'
            session['timelaps'] = 1
            fotos.ejecutarcomando(comando, False)
            print('Timelaps encendido')
        return render_template('timelaps.html', form=form, form2=form2)


@login_required
@core.route('/mensajeadm',methods=['GET','POST'])
def mensajeadm():
    lista_msg = []
    listado = MensajesAdm.query.filter_by(usuario=session['username']).order_by(MensajesAdm.id.asc()).all()

    con = Conexion2()
    try:
        for i in listado:
            print(i.id_mensaje)

            consulta = """SELECT respuesta FROM mensajesadmserver WHERE id_mensaje = '%s'""" % i.id_mensaje
            con.CUR.execute(consulta)
            i.respuesta = con.CUR.fetchone()
            print(i.respuesta)
            MensajesAdm.query.filter_by(id_mensaje=i.id_mensaje).update(
                {MensajesAdm.respuesta: i.respuesta}, synchronize_session=False)
            db.session.commit()
            data = {i.id_mensaje:i.respuesta}
            lista_msg.append(data)

    except:
        pass
    #con.CUR.close()
    print(lista_msg)

    msg = ParamikoComando()
    msg.conectar()
    comando = 'raspip.py'
    stdin, stdout, stderr = msg.ejecutarcomando(comando, True)
    ip = str(stdout.readlines()[0])
    print(ip)
    comando = 'nserie.py'
    stdin, stdout, stderr = msg.ejecutarcomando(comando, False)
    numero_serie_rpi = str(stdout.readlines()[0])
    print(numero_serie_rpi)
    fecha = datetime.now().date()
    hora = datetime.now().time()
    form = MensajeAdminForm()
    if form.validate_on_submit():
        mensaje = form.mensaje.data
        asunto = form.asunto.data
        mensaje_a_base = MensajesAdm(fecha,hora,asunto,mensaje,numero_serie_rpi,ip,session['username'])

        #con = Conexion2()
        id_mensaje = mensaje_a_base.id_mensaje
        datos = (fecha,hora,asunto,mensaje,numero_serie_rpi,ip,session['username'],id_mensaje)
        consulta ="""INSERT INTO  mensajesadmserver (fecha, hora, asunto, mensaje, numero_serie_rpi, ip_rpi, usuario, id_mensaje) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"""
        try:
            con.CUR.execute(consulta, datos)
            con.CONEXION.commit()

            db.session.add(mensaje_a_base)
            db.session.commit()
         #   con.CUR.close()
            flash('Mensaje enviado al administrador, en breve sera respondido','info')
        except:
          #  con.CUR.close()
            flash('Mensaje no enviado, intente mas tarde','warning')
        return redirect(url_for('.home', user = session['username']))
    return render_template('mensajes.html',form = form, ip = ip, numero_serie_rpi = numero_serie_rpi, fecha = fecha, hora = hora, listado = listado)
