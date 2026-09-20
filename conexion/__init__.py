# conexion/__init__.py
# CSi - CoFre Sistemas Informáticos
# Semana 13: paquete que centraliza la conexión con la base de datos
# relacional (PostgreSQL). Se expone obtener_conexion() para que app.py
# no tenga que conocer los detalles de psycopg2 ni las credenciales.

from .conexion import obtener_conexion, crear_base_datos_si_no_existe

__all__ = ['obtener_conexion', 'crear_base_datos_si_no_existe']
