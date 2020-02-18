from flask import Blueprint,render_template,url_for,redirect,request,session,flash
from flask_login import login_required
from werkzeug.utils import secure_filename
from src import app,db
from src.core.forms import Ejecutar,Seleccionar,Parar,IndoorForm,AutomaticForm, TrabajandoForm,MensajeAdminForm
import paramiko
import time
from time import sleep
from datetime import datetime
import os
from src.comando import ParamikoComando
from src.models import Configuracion, Historial, Luna, Sensordht22,SensorStream, MensajesAdm, SensorPhStream, SensorHumSueloStream
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

intractor = ParamikoComando()#modificar
#intractor_extractor = ParamikoComando()
#ventilacion.conectar()

extractor = ParamikoComando()#modificar
#ec_up = ParamikoComando()
#extractor.conectar()

ventilador = ParamikoComando()

ph_down = ParamikoComando()
#ec_down = ParamikoComando()

ph_up = ParamikoComando()

servicios = [luz,humedad,riego,intractor,extractor,ventilador,ph_down,ph_up]#modificar
#servicios = [luz,humedad,riego,intractor_extractor,ec_up,ventilador,ec_down,ph_up]#modificar

#################################
#################################
###########GLOBALS###############
ban_luz = False
ban_int = False#modificar ban_ext_int
ban_hum = False
ban_rie = False
ban_ext = False#modificar ban_ec_up
ban_ven = False
ban_ph_up = False
ban_ph_down = False#modificar x ban_ec_down
TRABAJANDO = False
INSTANCIAS = True
BANDERAS = []
HUMEDAD = ''
TEMPERATURA = ''
PH = 0
SUELO = 0
#EC = 0
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
            #session['ec_min'] = confi.ec_min
            #session['ec_max'] = confi.ec_max
            session['trabajando'] = True
            session['inicio'] = confi.inicio

            return True
        else:
            TRABAJANDO = False
            session['trabajando'] = False
        automatic.client.close()
    except:
        pass

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
    global TRABAJANDO, INSTANCIAS, HUMEDAD, TEMPERATURA, PH, SUELO #,EC agregar EC en este endpoint y en los templates renderizados
    #estado_suelo = 'Seco' if SUELO > 0.4 else 'Humedo'
    estado_suelo = SUELO
    ultima_c = Historial.query.order_by(Historial.id.desc()).first()
    session['nombre_conf'] = ultima_c.nombre_conf
    comprobar_automatic()
    comprobar_ecosystem()

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

    return render_template('home.html',user=user, TRABAJANDO=TRABAJANDO,form=form,humedad=HUMEDAD,temperatura=TEMPERATURA, ph=PH, suelo=estado_suelo)

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
    HOST = '192.168.0.103'
    USERNAME = 'mrthc'
    PASSWORD = '1qaz2wsx3EDC4RFV.'
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
    global ban_hum,ban_int,ban_rie,ban_luz,ban_ext,ban_ven,ban_ph_down,ban_ph_up,t,TRABAJANDO, INSTANCIAS, BANDERAS
    #global ban_hum,ban_int_ext,ban_rie,ban_luz,ban_ec_up,ban_ven,ban_ec_down,ban_ph_up,t,TRABAJANDO, INSTANCIAS, BANDERAS

    comandos = ['apagar_proceso1.py','apagar_proceso2.py','apagar_proceso3.py','apagar_proceso4.py','apagar_proceso5.py','apagar_proceso6.py','apagar_proceso7.py','apagar_proceso8.py']
    form = IndoorForm()
    flash('CUIDADO SE APAGARA EL PROCESO AUTOMATICO O LOS PROCESOS QUE ESTAN EN EJECUCION','danger')

    if form.salir.data == True and BANDERAS == []:
        return redirect(url_for('.home', user=session['username']))

    if form.validate_on_submit() and form.salir.data == False:
        TRABAJANDO = False

        if comprobar_automatic():
            liberar_gpios()
            matar_automatic()
            matar_datosdh22()
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
########cambiar form.intractor.data por form.intractor_extractor.data
        if form.intractor.data == True:
            intractor.conectar()
            print('Intractor encendido')
            comando = 'proceso2.py'
            stdin, stdout, stderr = intractor.ejecutarcomando(comando,True)
            form.intractor.data = False
            ban_int = True
            BANDERAS.append(1)
        if form.a_intractor.data == True:
            print('Intractor apagado')

            comando = comandos[1]
            stdin, stdout, stderr = intractor.ejecutarcomando(comando, False)

            intractor.client.close()
            form.a_intractor.data = False
            intractor.conectar()
            ban_int = False
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
        if form.extractor.data == True:
            extractor.conectar()
            print('Extractor encendido')
            comando = 'proceso5.py'
            stdin, stdout, stderr = extractor.ejecutarcomando(comando,True)
            form.extractor.data = False
            ban_ext = True
            BANDERAS.append(1)
        if form.a_extractor.data == True:
            print('Extractor apagado')

            comando = comandos[4]
            stdin, stdout, stderr = extractor.ejecutarcomando(comando, False)

            extractor.client.close()
            form.a_extractor.data = False
            extractor.conectar()
            ban_ext = False
            BANDERAS.append(1)
############################################################################
        if form.ventilador.data == True:
            ventilador.conectar()
            print('Ventilador encendido')
            comando = 'proceso6.py'
            stdin, stdout, stderr = ventilador.ejecutarcomando(comando,True)
            form.ventilador.data = False
            ban_ven = True
            BANDERAS.append(1)
        if form.a_ventilador.data == True:
            print('Ventilador apagado')

            comando = comandos[5]
            stdin, stdout, stderr = ventilador.ejecutarcomando(comando, False)

            ventilador.client.close()
            form.a_ventilador.data = False
            ventilador.conectar()
            ban_ven = False
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

        if form.ph_down.data == True:
            ph_down.conectar()
            print('Bajando ph')
            comando = 'proceso8.py'
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
            ban_int = False
            ban_hum = False
            ban_rie = False
            ban_ext = False
            ban_ven = False
            ban_ph_down =False
            ban_ph_up = False
            liberar_gpios()
        except:
            pass
        finally:
            return redirect(url_for('.home',user=session['username']))

    return render_template('indoor.html',form = form, ban_luz = ban_luz, ban_rie = ban_rie, ban_int = ban_int, ban_hum = ban_hum, ban_ext = ban_ext, ban_ven = ban_ven, ban_ph_down = ban_ph_down, ban_ph_up = ban_ph_up)


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
        nombre = form.nombre_conf.data
        ph_min = float(form.ph_min.data)
        ph_max = float(form.ph_max.data)
        print('aca va el de humedad del suelo')
        print(form.hum_suelo.data)

        if form.check_conf(nombre):
            flash('Ya existe una configuracion con ese nombre, desea sobreescribirla?','warning')
            return render_template('borrar_actualizar.html',luz=form.luz.data, humedad_suelo=form.humedad_suelo.data,riego=form.riego.data,cantidad_riego=form.cantidad_riego.data, humedad_min=form.humedad_min.data,humedad_max=form.humedad_max.data,temperatura_min=form.temperatura_min.data,temperatura_max=form.temperatura_max.data,nombre_conf = form.nombre_conf.data,ventilador = form.ventilador.data, cantidad_ventilador = form.cantidad_ventilador.data, ph_min = ph_min, ph_max = ph_max)
        else:
            if form.hum_suelo.data == True:
                form.riego.data = 0
                form.cantidad_riego.data = 0
            else:
                form.humedad_suelo.data = 0
            configuracion = Configuracion(
                luz=form.luz.data, humedad_suelo=form.humedad_suelo.data,riego=form.riego.data,cantidad_riego=form.cantidad_riego.data, humedad_min=form.humedad_min.data,humedad_max=form.humedad_max.data,
                temperatura_min=form.temperatura_min.data,temperatura_max=form.temperatura_max.data, nombre_conf = form.nombre_conf.data, ventilador = form.ventilador.data, cantidad_ventilador = form.cantidad_ventilador.data,
                ph_min = ph_min, ph_max = ph_max
            )
            db.session.add(configuracion)
            db.session.commit()
            encender_sensorDHT22()
            ejecutar_automatic(nombre_conf=nombre)

            return redirect(url_for('.home',user = session['username']))
    return render_template('automatico.html',form = form )


@login_required
@core.route('/update/<string:nombre_conf>/<int:luz>/<int:temperatura_min>/<int:temperatura_max>/<int:riego>/<int:cantidad_riego>/<int:humedad_min>/<int:humedad_max>/<int:ventilador>/<int:cantidad_ventilador>/<float:ph_min>/<float:ph_max>/<int:humedad_suelo>', methods=['GET','POST'])
def update(nombre_conf,luz,temperatura_min,temperatura_max,riego,cantidad_riego,humedad_min,humedad_max,ventilador,cantidad_ventilador,ph_min,ph_max,humedad_suelo):
    global TRABAJANDO, INSTANCIAS

    matar_instancias()
    liberar_gpios()
    matar_automatic()
    matar_datosdh22()
    if humedad_suelo != 0 and humedad_suelo != 1:
        riego = 0
        cantidad_riego = 0
    if humedad_suelo == 1:
        humedad_suelo = 0
    session['inicio'] = datetime.now()
    Configuracion.query.filter_by(nombre_conf=nombre_conf).update(
        {Configuracion.luz: luz, Configuracion.humedad_suelo: humedad_suelo, Configuracion.riego: riego, Configuracion.cantidad_riego: cantidad_riego ,Configuracion.temperatura_min: temperatura_min, Configuracion.temperatura_max: temperatura_max, Configuracion.humedad_min: humedad_min, Configuracion.humedad_max: humedad_max, Configuracion.ventilador: ventilador, Configuracion.cantidad_ventilador:cantidad_ventilador, Configuracion.ph_min:ph_min, Configuracion.ph_max:ph_max, Configuracion.inicio:session['inicio']}, synchronize_session=False)
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
    comando = 'luna.py'
    stdin, stdout, stderr = proceso.ejecutarcomando(comando, False)
    print('comando '+comando+' ejecutado')
    #aca va un sleep porque el tiempo de la consulta es mas corto que la ejecuciond el script luna.py y sale error porque no encuentra nada la primera vez
    luna_hoy = Luna.query.filter_by(id=1).first()
    luna_fases = Luna.query.all()
    dia = str(datetime.today().day)
    mes = str(datetime.today().month)
    anio = str(datetime.today().year)
    print(dia+'/'+mes+'/'+anio)
    img_nueva = Luna.query.filter(Luna.fase=='Luna Nueva').first()
    img_llena = Luna.query.filter(Luna.fase=='Luna Llena').first()
    img_creciente = Luna.query.filter(Luna.fase=='Cuarto Creciente').first()
    img_menguante = Luna.query.filter(Luna.fase=='Cuarto Menguante').first()
    nueva = base64.b64encode(img_nueva.image).decode('ascii')
    llena = base64.b64encode(img_llena.image).decode('ascii')
    creciente = base64.b64encode(img_creciente.image).decode('ascii')
    menguante = base64.b64encode(img_menguante.image).decode('ascii')

    return render_template('luna.html',luna_hoy = luna_hoy, luna_fases = luna_fases, dia =dia, mes = mes, anio = anio,
                           creciente = creciente,llena=llena,menguante=menguante,nueva=nueva)


@login_required
@core.route('/sensor')
def sensor():
    global HUMEDAD,TEMPERATURA,PH,SUELO
    consulta = SensorStream.query.order_by(SensorStream.id.desc()).first()
    HUMEDAD = consulta.hum
    TEMPERATURA = consulta.temp
    consulta_ph = SensorPhStream.query.order_by(SensorPhStream.id.desc()).first()
    PH = consulta_ph.ph
    consulta_suelo = SensorHumSueloStream.query.order_by(SensorHumSueloStream.id.desc()).first()
    SUELO = consulta_suelo.hum_suelo

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
        camara.client.close()
        print('camara apagada')
    else:
        print('camara encendida')

    return redirect(url_for('.home',user = session['username']))

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
