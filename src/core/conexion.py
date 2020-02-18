import psycopg2

class Conexion2:
    try:
        CONEXION = psycopg2.connect(host='192.168.0.101', port=5432, database='rserver', user='martincholoco',
                                    password='1qaz2wsx')
        CUR = CONEXION.cursor()

    except:
        pass