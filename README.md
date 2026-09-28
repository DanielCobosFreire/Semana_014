# CSi - CoFre Sistemas Informáticos

## Proyecto Integrador U4 - Semana 15 / Avance 15 de 16

Aplicación web desarrollada con **Flask + PostgreSQL** para la gestión administrativa de
CSi - CoFre Sistemas Informáticos.

Este avance continúa el sistema de autenticación de la Semana 14 y completa las
operaciones **CRUD (Create, Read, Update, Delete)** conectadas a PostgreSQL.

## Funcionalidades implementadas

- Login y registro con **Flask-Login**.
- Contraseñas almacenadas mediante **Werkzeug password hashing**.
- Rutas administrativas protegidas con **@login_required**.
- Protección **CSRF** con Flask-WTF.
- Consultas SQL **parametrizadas** con psycopg2.
- CRUD completo de:
  - Productos.
  - Clientes.
  - Proveedores.
  - Facturas.
- Formularios validados con WTForms.
- Listados mediante tablas HTML.
- PostgreSQL como sistema de persistencia.
- Relaciones mediante PRIMARY KEY y FOREIGN KEY.
- Consulta JOIN para información relacionada.
- Configuración compatible con Render mediante **DATABASE_URL**.
- Gunicorn como servidor WSGI para producción.

## Modelo relacional

Relaciones principales:

```text
PROVEEDORES (id_proveedor PK)
        |
        | 1 : N
        v
PRODUCTOS (id_producto PK, id_proveedor FK)

CLIENTES (id_cliente PK)
        |
        | 1 : N
        v
FACTURAS (id_factura PK, id_cliente FK)

USUARIOS (id PK)
```

La aplicación contiene más de las tres tablas relacionadas exigidas por la actividad.

## JOIN utilizado

El módulo de Facturación muestra el cliente asociado a cada factura mediante:

```sql
SELECT f.id_factura, f.numero, f.fecha, f.total, f.estado,
       f.id_cliente,
       COALESCE(c.nombre, 'Cliente eliminado') AS cliente,
       c.empresa
FROM facturas f
LEFT JOIN clientes c
    ON f.id_cliente = c.id_cliente
ORDER BY f.id_factura;
```

Productos también utiliza una relación entre `productos` y `proveedores`.

## Operaciones CRUD

Cada módulo implementa:

```text
CREAR       -> INSERT
LEER        -> SELECT
ACTUALIZAR  -> UPDATE
ELIMINAR    -> DELETE
```

Todas las operaciones reciben parámetros mediante placeholders `%s`, evitando concatenar
directamente datos provenientes de formularios.

## Configuración local

### 1. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 2. Configurar variables

Copiar:

```bash
cp .env.example .env
```

Editar `.env` según la instalación local de PostgreSQL.

Ejemplo:

```env
SECRET_KEY=una-clave-local
DB_HOST=localhost
DB_PORT=5432
DB_NAME=csi_ferreteria
DB_USER=csi_user
DB_PASSWORD=csi_password
```

El archivo `.env` está excluido mediante `.gitignore`.

### 3. Ejecutar

```bash
python app.py
```

Abrir:

```text
http://127.0.0.1:5000
```

## Despliegue en Render

El repositorio incluye `render.yaml`.

Configuración principal:

```text
Build Command:
pip install -r requirements.txt

Start Command:
gunicorn app:app
```

En Render deben existir:

- un Web Service;
- una base de datos PostgreSQL;
- `DATABASE_URL`;
- `SECRET_KEY`.

Cuando `DATABASE_URL` está definida, la aplicación utiliza directamente la base PostgreSQL
de Render. Si no está definida, utiliza las variables `DB_*` del entorno local.

## Prueba obligatoria Semana 15

Realizar desde la aplicación desplegada en Render:

1. Abrir la aplicación.
2. Registrar un usuario si todavía no existe.
3. Iniciar sesión.
4. Ingresar a Clientes.
5. Listar registros.
6. Agregar un nuevo cliente.
7. Modificar el cliente.
8. Eliminar un registro de prueba.
9. Ingresar a Productos y comprobar el CRUD.
10. Ingresar a Proveedores y comprobar el CRUD.
11. Crear una factura seleccionando un cliente.
12. Abrir Facturación y comprobar el JOIN Cliente - Factura.
13. Modificar la factura.
14. Eliminar una factura de prueba.
15. Cerrar sesión.
16. Intentar abrir una ruta administrativa y comprobar la redirección al login.

Secuencia solicitada por la rúbrica:

```text
Login -> Listar -> Agregar -> Modificar -> Eliminar
      -> Consultar información relacionada -> Cerrar sesión
```

## Archivos principales

```text
app.py
models.py
requirements.txt
render.yaml
.env.example
.gitignore

conexion/
  conexion.py

sql/
  esquema.sql

forms/
  producto_form.py
  cliente_form.py
  proveedor_form.py
  facturacion_form.py
  login_form.py
  usuario_form.py

templates/
  login.html
  registro.html
  dashboard.html
  productos.html
  clientes.html
  proveedores.html
  facturacion.html
  formulario_producto.html
  formulario_cliente.html
  formulario_proveedor.html
  formulario_facturacion.html
```

## Cumplimiento de la rúbrica

| Requisito | Estado |
|---|---|
| Flask | Cumple |
| PostgreSQL | Cumple |
| 3 o más tablas relacionadas | Cumple |
| PRIMARY KEY | Cumple |
| FOREIGN KEY | Cumple |
| CREATE / INSERT | Cumple |
| READ / SELECT | Cumple |
| UPDATE | Cumple |
| DELETE | Cumple |
| Formularios | Cumple |
| Validaciones | Cumple |
| Tablas HTML | Cumple |
| Consulta JOIN | Cumple |
| Login Semana 14 | Cumple |
| @login_required | Cumple |
| CSRF | Cumple |
| SQL parametrizado | Cumple |
| requirements.txt actualizado | Cumple |
| Configuración Render | Preparada |
| PostgreSQL en Render | Preparada mediante DATABASE_URL |

---

**Universidad Estatal Amazónica - Tecnologías de la Información**

Proyecto: **CSi - CoFre Sistemas Informáticos**
