# conexion/conexion.py
# CSi - CoFre Sistemas Informáticos
# Semana 13: conexión centralizada con una base de datos relacional.
# Se eligió PostgreSQL (opción B de la consigna) usando psycopg2-binary.
# Semana 14: las credenciales ahora se leen con python-dotenv desde un
# archivo .env local (que NUNCA se sube al repositorio, ver .gitignore),
# usando .env.example como plantilla. También se agrega
# inicializar_base_datos_si_no_existe(), que crea la base de datos por
# nombre si todavía no existe, para que el proyecto funcione con un solo
# "python app.py" apenas se instala PostgreSQL.

import os

import psycopg2
import psycopg2.extras
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from dotenv import load_dotenv

# Carga variables desde un archivo .env si existe (no falla si no existe:
# en ese caso simplemente se usan los valores por defecto de abajo).
load_dotenv()

# Semana 13/14: parámetros de conexión. Se pueden sobreescribir con
# variables de entorno (típicamente definidas en un archivo .env que NO
# se sube al repositorio) sin tener que tocar el código.
CONFIG_DB = {
    'host': os.environ.get('DB_HOST', 'localhost'),
    'port': os.environ.get('DB_PORT', '5432'),
    'dbname': os.environ.get('DB_NAME', 'csi_ferreteria'),
    'user': os.environ.get('DB_USER', 'csi_user'),
    'password': os.environ.get('DB_PASSWORD', 'csi_password'),
}


def obtener_conexion():
    """Abre y devuelve una nueva conexión a PostgreSQL.

    Se usa cursor_factory=RealDictCursor para que cada fila se comporte
    como un diccionario (fila['nombre'] o fila.get('nombre')), lo que
    permite reutilizar exactamente la misma sintaxis Jinja2 de semanas
    anteriores en las plantillas ({{ producto.nombre }}, etc.).

    Quien llama a esta función es responsable de cerrar la conexión con
    conn.close() (y el cursor, si lo abrió explícitamente) una vez
    terminadas sus operaciones, tal como pide la consigna de la Semana 13.
    """
    return psycopg2.connect(
        host=CONFIG_DB['host'],
        port=CONFIG_DB['port'],
        dbname=CONFIG_DB['dbname'],
        user=CONFIG_DB['user'],
        password=CONFIG_DB['password'],
        cursor_factory=psycopg2.extras.RealDictCursor,
    )


def crear_base_datos_si_no_existe():
    """Semana 14: comodidad para desarrollo local. Se conecta a la base
    de mantenimiento 'postgres' del mismo servidor y crea CONFIG_DB['dbname']
    si todavía no existe, para que baste con tener PostgreSQL instalado
    (sin crear la base de datos a mano) para correr 'python app.py'.
    Si algo falla aquí (por permisos, por ejemplo), no se interrumpe el
    arranque: se asume que la base de datos ya existe y se sigue adelante."""
    try:
        conn = psycopg2.connect(
            host=CONFIG_DB['host'],
            port=CONFIG_DB['port'],
            dbname='postgres',
            user=CONFIG_DB['user'],
            password=CONFIG_DB['password'],
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        with conn.cursor() as cur:
            cur.execute('SELECT 1 FROM pg_database WHERE datname = %s', (CONFIG_DB['dbname'],))
            if cur.fetchone() is None:
                cur.execute(f'CREATE DATABASE "{CONFIG_DB["dbname"]}"')
        conn.close()
    except Exception as error:
        print(f'[AVISO] No se pudo verificar/crear la base de datos automáticamente: {error}')
