-- sql/esquema.sql
-- CSi - CoFre Sistemas Informáticos
-- Semana 13: modelo relacional mínimo del Proyecto Integrador (PostgreSQL).
-- Semana 14: se agrega la tabla "usuarios" para el sistema de login
-- (Flask-Login + Werkzeug).
-- Permite recrear la estructura completa de la base de datos desde cero
-- ejecutando este archivo (por ejemplo con: psql -U csi_user -d csi_ferreteria -f sql/esquema.sql)
-- o dejando que app.py lo ejecute automáticamente al arrancar
-- (ver inicializar_base_datos() en app.py), gracias a CREATE TABLE IF NOT EXISTS.

-- ============================================================
-- Proveedores: entidad "padre" referenciada por productos.id_proveedor.
-- ============================================================
CREATE TABLE IF NOT EXISTS proveedores (
    id_proveedor SERIAL PRIMARY KEY,
    nombre       VARCHAR(120) NOT NULL,
    telefono     VARCHAR(20),
    correo       VARCHAR(120)
);

-- ============================================================
-- Productos: módulo con CRUD completo esta semana (SELECT, INSERT,
-- UPDATE, DELETE). id_proveedor es una FOREIGN KEY hacia proveedores;
-- puede ser NULL para productos tipo "Servicio" sin proveedor asociado.
-- ============================================================
CREATE TABLE IF NOT EXISTS productos (
    id_producto  SERIAL PRIMARY KEY,
    nombre       VARCHAR(100) NOT NULL,
    categoria    VARCHAR(50)  NOT NULL,
    precio       NUMERIC(10, 2) NOT NULL,
    stock        INTEGER,
    id_proveedor INTEGER REFERENCES proveedores(id_proveedor) ON DELETE SET NULL
);

-- ============================================================
-- Clientes: tabla preparada para incorporar su propio CRUD en un
-- avance posterior. Esta semana el módulo de Clientes sigue usando una
-- lista de Python en memoria (ver app.py), tal como permite la consigna.
-- ============================================================
CREATE TABLE IF NOT EXISTS clientes (
    id_cliente SERIAL PRIMARY KEY,
    nombre     VARCHAR(100) NOT NULL,
    cedula     VARCHAR(20),
    telefono   VARCHAR(20),
    correo     VARCHAR(120)
);

-- ============================================================
-- Facturas: tabla preparada, con FOREIGN KEY hacia clientes.id_cliente.
-- El módulo de Facturación sigue usando una lista de Python en memoria
-- esta semana; la tabla queda lista para conectarse en un avance futuro.
-- ============================================================
CREATE TABLE IF NOT EXISTS facturas (
    id_factura SERIAL PRIMARY KEY,
    id_cliente INTEGER REFERENCES clientes(id_cliente) ON DELETE SET NULL,
    fecha      DATE NOT NULL,
    total      NUMERIC(10, 2) NOT NULL
);

-- ============================================================
-- Semana 14: usuarios del sistema (autenticación con Flask-Login).
-- "usuario" es UNIQUE para evitar registros duplicados; "password"
-- NUNCA se guarda en texto plano: siempre se almacena el resultado de
-- generate_password_hash() (ver forms/usuario_form.py y la ruta /registro
-- en app.py). 255 caracteres es margen suficiente para un hash de
-- Werkzeug (scrypt/pbkdf2), que suele rondar los 100-130 caracteres.
-- ============================================================
CREATE TABLE IF NOT EXISTS usuarios (
    id       SERIAL PRIMARY KEY,
    usuario  VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL
);
