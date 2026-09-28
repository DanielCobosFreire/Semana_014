# app.py
# CSi - CoFre Sistemas Informáticos
# Proyecto Integrador U4 - Semana 15
# Flask + PostgreSQL + CRUD + JOIN + Login + CSRF + Render

import os
from datetime import datetime

import psycopg2
from flask import Flask, render_template, redirect, url_for, flash
from flask_login import (
    LoginManager, login_user, logout_user,
    login_required, current_user
)
from flask_wtf.csrf import CSRFProtect
from werkzeug.security import generate_password_hash, check_password_hash

from conexion import obtener_conexion, crear_base_datos_si_no_existe
from models import Usuario
from forms import (
    ProductoForm, ClienteForm, ProveedorForm, FacturacionForm,
    LoginForm, UsuarioForm,
)

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get(
    "SECRET_KEY", "csi-clave-solo-desarrollo-cambiar-en-produccion"
)

csrf = CSRFProtect(app)

login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.login_message = "Por favor inicia sesión para acceder a esta página."
login_manager.login_message_category = "warning"


@login_manager.user_loader
def load_user(user_id):
    return Usuario.obtener_por_id(user_id)


RUTA_ESQUEMA_SQL = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "sql", "esquema.sql"
)


def inicializar_base_datos():
    crear_base_datos_si_no_existe()
    conn = obtener_conexion()
    try:
        with conn:
            with conn.cursor() as cur:
                with open(RUTA_ESQUEMA_SQL, "r", encoding="utf-8") as archivo:
                    cur.execute(archivo.read())
        sembrar_datos_iniciales(conn)
    finally:
        conn.close()


def sembrar_datos_iniciales(conn):
    """Carga datos de demostración solo cuando cada tabla está vacía."""
    with conn.cursor() as cur:
        cur.execute("SELECT COUNT(*) AS total FROM proveedores")
        if cur.fetchone()["total"] == 0:
            cur.executemany(
                """
                INSERT INTO proveedores
                    (nombre, telefono, correo, producto, contacto)
                VALUES (%s, %s, %s, %s, %s)
                """,
                [
                    ("TecnoSuministros S.A.", "02-2345678",
                     "ventas@tecnosuministros.com", "Equipos de cómputo",
                     "ventas@tecnosuministros.com"),
                    ("DistriSoft Ecuador", "02-3456789",
                     "contacto@distrisoft.ec", "Licencias de software",
                     "contacto@distrisoft.ec"),
                    ("RedNet Cía. Ltda.", "02-4567890",
                     "info@rednet.ec", "Infraestructura de red",
                     "info@rednet.ec"),
                ],
            )

        cur.execute("SELECT COUNT(*) AS total FROM productos")
        if cur.fetchone()["total"] == 0:
            cur.execute("SELECT id_proveedor, nombre FROM proveedores")
            ids = {r["nombre"]: r["id_proveedor"] for r in cur.fetchall()}
            cur.executemany(
                """
                INSERT INTO productos
                    (nombre, categoria, precio, stock, id_proveedor)
                VALUES (%s, %s, %s, %s, %s)
                """,
                [
                    ('Laptop HP 15"', "Equipos", 650.00, 12,
                     ids.get("TecnoSuministros S.A.")),
                    ('Monitor LG 24"', "Equipos", 180.00, 20,
                     ids.get("TecnoSuministros S.A.")),
                    ("Licencia Windows 11 Pro", "Software", 199.00, 50,
                     ids.get("DistriSoft Ecuador")),
                    ("Servicio de Mantenimiento IT", "Servicios", 45.00, None, None),
                ],
            )

        cur.execute("SELECT COUNT(*) AS total FROM clientes")
        if cur.fetchone()["total"] == 0:
            cur.executemany(
                """
                INSERT INTO clientes
                    (nombre, empresa, correo, telefono, activo)
                VALUES (%s, %s, %s, %s, %s)
                """,
                [
                    ("Juan Pérez", "Ferretería El Tornillo",
                     "juan.perez@ejemplo.com", "0981234567", True),
                    ("María Torres", "Panadería Dulce Trigo",
                     "maria.torres@ejemplo.com", "0992345678", True),
                    ("Carlos Mendoza", "Colegio San Andrés",
                     "carlos.mendoza@ejemplo.com", "0983456789", False),
                ],
            )

        cur.execute("SELECT COUNT(*) AS total FROM facturas")
        if cur.fetchone()["total"] == 0:
            cur.execute("SELECT id_cliente, nombre FROM clientes")
            clientes = {r["nombre"]: r["id_cliente"] for r in cur.fetchall()}
            cur.executemany(
                """
                INSERT INTO facturas
                    (numero, id_cliente, fecha, total, estado)
                VALUES (%s, %s, %s, %s, %s)
                """,
                [
                    ("F-001", clientes.get("Juan Pérez"), "2026-08-01", 850.00, "Pagada"),
                    ("F-002", clientes.get("María Torres"), "2026-08-05", 199.00, "Pendiente"),
                    ("F-003", clientes.get("Carlos Mendoza"), "2026-08-10", 45.00, "Pagada"),
                ],
            )
    conn.commit()


inicializar_base_datos()


empresa_info = {
    "nombre": "CSi - CoFre Sistemas Informáticos",
    "slogan": "Consultoría tecnológica, desarrollo web, soporte TI y transformación digital.",
    "anio_fundacion": 2024,
    "mision": (
        "Optimizar procesos de empresas y emprendedores mediante herramientas "
        "digitales modernas, seguras y escalables."
    ),
    "servicios_destacados": [
        "Desarrollo Web", "Consultoría IT", "Soporte Técnico"
    ],
}


@app.context_processor
def inyectar_variables_globales():
    return {"anio_actual": datetime.now().year}


@app.route("/")
def index():
    return render_template("index.html", empresa=empresa_info)


# ---------------------------------------------------------------------------
# PRODUCTOS: CRUD PostgreSQL + JOIN con proveedores
# ---------------------------------------------------------------------------
@app.route("/productos")
@login_required
def productos():
    conn = obtener_conexion()
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT p.id_producto, p.nombre, p.categoria, p.precio, p.stock,
                   p.id_proveedor, pr.nombre AS proveedor_nombre
            FROM productos p
            LEFT JOIN proveedores pr
                ON p.id_proveedor = pr.id_proveedor
            ORDER BY p.id_producto
            """
        )
        filas = cur.fetchall()
    conn.close()
    return render_template("productos.html", productos=filas)


def _obtener_choices_proveedores():
    conn = obtener_conexion()
    with conn.cursor() as cur:
        cur.execute(
            "SELECT id_proveedor, nombre FROM proveedores ORDER BY nombre"
        )
        filas = cur.fetchall()
    conn.close()
    return [("", "Sin proveedor asignado")] + [
        (str(r["id_proveedor"]), r["nombre"]) for r in filas
    ]


@app.route("/productos/nuevo", methods=["GET", "POST"])
@app.route("/productos/editar/<int:producto_id>", methods=["GET", "POST"])
@login_required
def formulario_producto(producto_id=None):
    conn = obtener_conexion()

    if producto_id is not None:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT * FROM productos WHERE id_producto = %s",
                (producto_id,),
            )
            fila = cur.fetchone()
        if fila is None:
            conn.close()
            flash("El producto solicitado no existe.", "danger")
            return redirect(url_for("productos"))

        datos = dict(fila)
        datos["proveedor"] = (
            str(datos["id_proveedor"])
            if datos["id_proveedor"] is not None else ""
        )
        form = ProductoForm(data=datos)
    else:
        form = ProductoForm()

    form.proveedor.choices = _obtener_choices_proveedores()

    if form.validate_on_submit():
        id_proveedor = int(form.proveedor.data) if form.proveedor.data else None
        with conn.cursor() as cur:
            if producto_id is None:
                cur.execute(
                    """
                    INSERT INTO productos
                        (nombre, categoria, precio, stock, id_proveedor)
                    VALUES (%s, %s, %s, %s, %s)
                    """,
                    (
                        form.nombre.data, form.categoria.data,
                        form.precio.data, form.stock.data, id_proveedor,
                    ),
                )
                mensaje = "Producto registrado correctamente."
            else:
                cur.execute(
                    """
                    UPDATE productos
                    SET nombre=%s, categoria=%s, precio=%s,
                        stock=%s, id_proveedor=%s
                    WHERE id_producto=%s
                    """,
                    (
                        form.nombre.data, form.categoria.data,
                        form.precio.data, form.stock.data,
                        id_proveedor, producto_id,
                    ),
                )
                mensaje = "Producto actualizado correctamente."
        conn.commit()
        conn.close()
        flash(mensaje, "success")
        return redirect(url_for("productos"))

    conn.close()
    return render_template(
        "formulario_producto.html", form=form, indice=producto_id
    )


@app.route("/productos/eliminar/<int:producto_id>", methods=["POST"])
@login_required
def eliminar_producto(producto_id):
    conn = obtener_conexion()
    with conn.cursor() as cur:
        cur.execute(
            "SELECT nombre FROM productos WHERE id_producto=%s",
            (producto_id,),
        )
        fila = cur.fetchone()
        if fila is None:
            conn.close()
            flash("El producto no existe o ya fue eliminado.", "warning")
            return redirect(url_for("productos"))
        cur.execute(
            "DELETE FROM productos WHERE id_producto=%s",
            (producto_id,),
        )
    conn.commit()
    conn.close()
    flash(f'Producto "{fila["nombre"]}" eliminado correctamente.', "success")
    return redirect(url_for("productos"))


# ---------------------------------------------------------------------------
# CLIENTES: CRUD PostgreSQL
# ---------------------------------------------------------------------------
@app.route("/clientes")
@login_required
def clientes():
    conn = obtener_conexion()
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT id_cliente, nombre, empresa, correo, telefono, activo
            FROM clientes
            ORDER BY id_cliente
            """
        )
        filas = cur.fetchall()
    conn.close()
    return render_template("clientes.html", clientes=filas)


@app.route("/clientes/nuevo", methods=["GET", "POST"])
@app.route("/clientes/editar/<int:cliente_id>", methods=["GET", "POST"])
@login_required
def formulario_cliente(cliente_id=None):
    conn = obtener_conexion()

    if cliente_id is not None:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT id_cliente, nombre, empresa, correo, telefono, activo
                FROM clientes WHERE id_cliente=%s
                """,
                (cliente_id,),
            )
            fila = cur.fetchone()
        if fila is None:
            conn.close()
            flash("El cliente solicitado no existe.", "danger")
            return redirect(url_for("clientes"))
        form = ClienteForm(data=dict(fila))
    else:
        form = ClienteForm()

    if form.validate_on_submit():
        with conn.cursor() as cur:
            if cliente_id is None:
                cur.execute(
                    """
                    INSERT INTO clientes
                        (nombre, empresa, correo, telefono, activo)
                    VALUES (%s, %s, %s, %s, %s)
                    """,
                    (
                        form.nombre.data, form.empresa.data,
                        form.correo.data, form.telefono.data,
                        form.activo.data,
                    ),
                )
                mensaje = "Cliente registrado correctamente."
            else:
                cur.execute(
                    """
                    UPDATE clientes
                    SET nombre=%s, empresa=%s, correo=%s,
                        telefono=%s, activo=%s
                    WHERE id_cliente=%s
                    """,
                    (
                        form.nombre.data, form.empresa.data,
                        form.correo.data, form.telefono.data,
                        form.activo.data, cliente_id,
                    ),
                )
                mensaje = "Cliente actualizado correctamente."
        conn.commit()
        conn.close()
        flash(mensaje, "success")
        return redirect(url_for("clientes"))

    conn.close()
    return render_template(
        "formulario_cliente.html", form=form, indice=cliente_id
    )


@app.route("/clientes/eliminar/<int:cliente_id>", methods=["POST"])
@login_required
def eliminar_cliente(cliente_id):
    conn = obtener_conexion()
    with conn.cursor() as cur:
        cur.execute(
            "SELECT nombre FROM clientes WHERE id_cliente=%s",
            (cliente_id,),
        )
        fila = cur.fetchone()
        if fila is None:
            conn.close()
            flash("El cliente no existe o ya fue eliminado.", "warning")
            return redirect(url_for("clientes"))
        cur.execute(
            "DELETE FROM clientes WHERE id_cliente=%s",
            (cliente_id,),
        )
    conn.commit()
    conn.close()
    flash(f'Cliente "{fila["nombre"]}" eliminado correctamente.', "success")
    return redirect(url_for("clientes"))


# ---------------------------------------------------------------------------
# PROVEEDORES: CRUD PostgreSQL
# ---------------------------------------------------------------------------
@app.route("/proveedores")
@login_required
def proveedores():
    conn = obtener_conexion()
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT id_proveedor, nombre,
                   COALESCE(producto, '') AS producto,
                   COALESCE(contacto, correo, '') AS contacto
            FROM proveedores
            ORDER BY id_proveedor
            """
        )
        filas = cur.fetchall()
    conn.close()
    return render_template("proveedores.html", proveedores=filas)


@app.route("/proveedores/nuevo", methods=["GET", "POST"])
@app.route("/proveedores/editar/<int:proveedor_id>", methods=["GET", "POST"])
@login_required
def formulario_proveedor(proveedor_id=None):
    conn = obtener_conexion()

    if proveedor_id is not None:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT id_proveedor, nombre,
                       COALESCE(producto, '') AS producto,
                       COALESCE(contacto, correo, '') AS contacto
                FROM proveedores WHERE id_proveedor=%s
                """,
                (proveedor_id,),
            )
            fila = cur.fetchone()
        if fila is None:
            conn.close()
            flash("El proveedor solicitado no existe.", "danger")
            return redirect(url_for("proveedores"))
        form = ProveedorForm(data=dict(fila))
    else:
        form = ProveedorForm()

    if form.validate_on_submit():
        with conn.cursor() as cur:
            if proveedor_id is None:
                cur.execute(
                    """
                    INSERT INTO proveedores
                        (nombre, producto, contacto, correo)
                    VALUES (%s, %s, %s, %s)
                    """,
                    (
                        form.nombre.data, form.producto.data,
                        form.contacto.data, form.contacto.data,
                    ),
                )
                mensaje = "Proveedor registrado correctamente."
            else:
                cur.execute(
                    """
                    UPDATE proveedores
                    SET nombre=%s, producto=%s, contacto=%s, correo=%s
                    WHERE id_proveedor=%s
                    """,
                    (
                        form.nombre.data, form.producto.data,
                        form.contacto.data, form.contacto.data,
                        proveedor_id,
                    ),
                )
                mensaje = "Proveedor actualizado correctamente."
        conn.commit()
        conn.close()
        flash(mensaje, "success")
        return redirect(url_for("proveedores"))

    conn.close()
    return render_template(
        "formulario_proveedor.html", form=form, indice=proveedor_id
    )


@app.route("/proveedores/eliminar/<int:proveedor_id>", methods=["POST"])
@login_required
def eliminar_proveedor(proveedor_id):
    conn = obtener_conexion()
    with conn.cursor() as cur:
        cur.execute(
            "SELECT nombre FROM proveedores WHERE id_proveedor=%s",
            (proveedor_id,),
        )
        fila = cur.fetchone()
        if fila is None:
            conn.close()
            flash("El proveedor no existe o ya fue eliminado.", "warning")
            return redirect(url_for("proveedores"))
        cur.execute(
            "DELETE FROM proveedores WHERE id_proveedor=%s",
            (proveedor_id,),
        )
    conn.commit()
    conn.close()
    flash(f'Proveedor "{fila["nombre"]}" eliminado correctamente.', "success")
    return redirect(url_for("proveedores"))


# ---------------------------------------------------------------------------
# FACTURACIÓN: CRUD PostgreSQL + JOIN con clientes
# ---------------------------------------------------------------------------
def _obtener_choices_clientes():
    conn = obtener_conexion()
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT id_cliente, nombre, empresa
            FROM clientes
            ORDER BY nombre
            """
        )
        filas = cur.fetchall()
    conn.close()
    return [
        (
            str(r["id_cliente"]),
            f'{r["nombre"]} - {r["empresa"]}' if r["empresa"] else r["nombre"],
        )
        for r in filas
    ]


@app.route("/facturacion")
@login_required
def facturacion():
    conn = obtener_conexion()
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT f.id_factura, f.numero, f.fecha, f.total, f.estado,
                   f.id_cliente,
                   COALESCE(c.nombre, 'Cliente eliminado') AS cliente,
                   c.empresa
            FROM facturas f
            LEFT JOIN clientes c
                ON f.id_cliente = c.id_cliente
            ORDER BY f.id_factura
            """
        )
        filas = cur.fetchall()
    conn.close()
    return render_template("facturacion.html", facturas=filas)


@app.route("/facturacion/nueva", methods=["GET", "POST"])
@app.route("/facturacion/editar/<int:factura_id>", methods=["GET", "POST"])
@login_required
def formulario_facturacion(factura_id=None):
    conn = obtener_conexion()

    if factura_id is not None:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT * FROM facturas WHERE id_factura=%s",
                (factura_id,),
            )
            fila = cur.fetchone()
        if fila is None:
            conn.close()
            flash("La factura solicitada no existe.", "danger")
            return redirect(url_for("facturacion"))
        datos = dict(fila)
        datos["cliente"] = (
            str(datos["id_cliente"]) if datos["id_cliente"] is not None else ""
        )
        form = FacturacionForm(data=datos)
    else:
        form = FacturacionForm()

    form.cliente.choices = _obtener_choices_clientes()

    if not form.cliente.choices:
        conn.close()
        flash(
            "Debe registrar al menos un cliente antes de crear una factura.",
            "warning",
        )
        return redirect(url_for("clientes"))

    if form.validate_on_submit():
        id_cliente = int(form.cliente.data)
        try:
            with conn.cursor() as cur:
                if factura_id is None:
                    cur.execute(
                        """
                        INSERT INTO facturas
                            (numero, id_cliente, fecha, total, estado)
                        VALUES (%s, %s, %s, %s, %s)
                        """,
                        (
                            form.numero.data, id_cliente, form.fecha.data,
                            form.total.data, form.estado.data,
                        ),
                    )
                    mensaje = "Factura registrada correctamente."
                else:
                    cur.execute(
                        """
                        UPDATE facturas
                        SET numero=%s, id_cliente=%s, fecha=%s,
                            total=%s, estado=%s
                        WHERE id_factura=%s
                        """,
                        (
                            form.numero.data, id_cliente, form.fecha.data,
                            form.total.data, form.estado.data, factura_id,
                        ),
                    )
                    mensaje = "Factura actualizada correctamente."
            conn.commit()
            flash(mensaje, "success")
            return redirect(url_for("facturacion"))
        except psycopg2.errors.UniqueViolation:
            conn.rollback()
            flash("Ya existe una factura con ese número.", "danger")
        finally:
            conn.close()

    else:
        conn.close()

    return render_template(
        "formulario_facturacion.html", form=form, indice=factura_id
    )


@app.route("/facturacion/eliminar/<int:factura_id>", methods=["POST"])
@login_required
def eliminar_factura(factura_id):
    conn = obtener_conexion()
    with conn.cursor() as cur:
        cur.execute(
            "SELECT numero FROM facturas WHERE id_factura=%s",
            (factura_id,),
        )
        fila = cur.fetchone()
        if fila is None:
            conn.close()
            flash("La factura no existe o ya fue eliminada.", "warning")
            return redirect(url_for("facturacion"))
        cur.execute(
            "DELETE FROM facturas WHERE id_factura=%s",
            (factura_id,),
        )
    conn.commit()
    conn.close()
    flash(f'Factura "{fila["numero"]}" eliminada correctamente.', "success")
    return redirect(url_for("facturacion"))


# ---------------------------------------------------------------------------
# AUTENTICACIÓN Semana 14, conservada en Semana 15
# ---------------------------------------------------------------------------
@app.route("/registro", methods=["GET", "POST"])
def registro():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard"))

    form = UsuarioForm()
    if form.validate_on_submit():
        password_hash = generate_password_hash(form.password.data)
        conn = obtener_conexion()
        try:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO usuarios (usuario, password)
                    VALUES (%s, %s)
                    """,
                    (form.usuario.data, password_hash),
                )
            conn.commit()
            flash(
                "Usuario registrado correctamente. Ya puedes iniciar sesión.",
                "success",
            )
            return redirect(url_for("login"))
        except psycopg2.errors.UniqueViolation:
            conn.rollback()
            flash("Ese nombre de usuario ya está en uso.", "danger")
        finally:
            conn.close()

    return render_template("registro.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard"))

    form = LoginForm()
    if form.validate_on_submit():
        usuario = Usuario.obtener_por_nombre_usuario(form.usuario.data)
        if usuario is not None and check_password_hash(
            usuario.password_hash, form.password.data
        ):
            login_user(usuario)
            flash(f"Bienvenido, {usuario.usuario}.", "success")
            return redirect(url_for("dashboard"))
        flash("Usuario o contraseña incorrectos.", "danger")

    return render_template("login.html", form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Sesión cerrada correctamente.", "success")
    return redirect(url_for("login"))


@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html")


if __name__ == "__main__":
    app.run(debug=True)
