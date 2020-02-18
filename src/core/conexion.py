import psycopg2

class Conexion2:
    try:
        CONEXION = psycopg2.connect(host='ip', port=5432, database='dbname', user='user',
                                    password='pass')
        CUR = CONEXION.cursor()

    except:
        pass