# models.py
# CSi - CoFre Sistemas Informáticos
# Semana 14: modelo de Usuario para el sistema de autenticación.
# No es un ORM completo: es un envoltorio ligero (UserMixin) alrededor
# de una fila de la tabla "usuarios" en PostgreSQL, tal como pide
# Flask-Login. UserMixin ya implementa is_authenticated, is_active,
# is_anonymous y get_id() a partir de self.id.

from flask_login import UserMixin

from conexion import obtener_conexion


class Usuario(UserMixin):
    """Representa un usuario autenticado del sistema."""

    def __init__(self, id_usuario, usuario, password_hash):
        self.id = id_usuario
        self.usuario = usuario
        self.password_hash = password_hash

    @staticmethod
    def obtener_por_id(user_id):
        """Usado por el user_loader de Flask-Login para reconstruir el
        usuario en cada request a partir del id guardado en la sesión."""
        conn = obtener_conexion()
        with conn.cursor() as cur:
            cur.execute('SELECT id, usuario, password FROM usuarios WHERE id = %s', (user_id,))
            fila = cur.fetchone()
        conn.close()

        if fila is None:
            return None
        return Usuario(fila['id'], fila['usuario'], fila['password'])

    @staticmethod
    def obtener_por_nombre_usuario(nombre_usuario):
        """Usado en la ruta /login para buscar las credenciales
        registradas antes de comprobar la contraseña con
        check_password_hash()."""
        conn = obtener_conexion()
        with conn.cursor() as cur:
            cur.execute('SELECT id, usuario, password FROM usuarios WHERE usuario = %s', (nombre_usuario,))
            fila = cur.fetchone()
        conn.close()

        if fila is None:
            return None
        return Usuario(fila['id'], fila['usuario'], fila['password'])
