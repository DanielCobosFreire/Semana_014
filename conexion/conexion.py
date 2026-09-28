# conexion/conexion.py
# CSi - CoFre Sistemas Informáticos
# Semana 15: conexión PostgreSQL compatible con desarrollo local y Render.

import os

import psycopg2
import psycopg2.extras
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.environ.get("DATABASE_URL")

CONFIG_DB = {
    "host": os.environ.get("DB_HOST", "localhost"),
    "port": os.environ.get("DB_PORT", "5432"),
    "dbname": os.environ.get("DB_NAME", "csi_ferreteria"),
    "user": os.environ.get("DB_USER", "csi_user"),
    "password": os.environ.get("DB_PASSWORD", "csi_password"),
}


def obtener_conexion():
    """Devuelve una conexión PostgreSQL usando RealDictCursor.

    En Render se usa DATABASE_URL. En desarrollo local se mantienen las
    variables DB_HOST, DB_PORT, DB_NAME, DB_USER y DB_PASSWORD.
    """
    if DATABASE_URL:
        return psycopg2.connect(
            DATABASE_URL,
            cursor_factory=psycopg2.extras.RealDictCursor,
        )

    return psycopg2.connect(
        host=CONFIG_DB["host"],
        port=CONFIG_DB["port"],
        dbname=CONFIG_DB["dbname"],
        user=CONFIG_DB["user"],
        password=CONFIG_DB["password"],
        cursor_factory=psycopg2.extras.RealDictCursor,
    )


def crear_base_datos_si_no_existe():
    """Crea la base local si hace falta.

    En Render la base PostgreSQL ya existe y DATABASE_URL apunta a ella,
    por lo que no se intenta ejecutar CREATE DATABASE.
    """
    if DATABASE_URL:
        return

    try:
        conn = psycopg2.connect(
            host=CONFIG_DB["host"],
            port=CONFIG_DB["port"],
            dbname="postgres",
            user=CONFIG_DB["user"],
            password=CONFIG_DB["password"],
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        with conn.cursor() as cur:
            cur.execute(
                "SELECT 1 FROM pg_database WHERE datname = %s",
                (CONFIG_DB["dbname"],),
            )
            if cur.fetchone() is None:
                cur.execute(f'CREATE DATABASE "{CONFIG_DB["dbname"]}"')
        conn.close()
    except Exception as error:
        print(f"[AVISO] No se pudo verificar/crear la base de datos: {error}")
