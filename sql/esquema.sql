-- sql/esquema.sql
-- CSi - CoFre Sistemas Informáticos
-- Semana 15: PostgreSQL + relaciones + CRUD + autenticación.

CREATE TABLE IF NOT EXISTS proveedores (
    id_proveedor SERIAL PRIMARY KEY,
    nombre       VARCHAR(120) NOT NULL,
    telefono     VARCHAR(20),
    correo       VARCHAR(120),
    producto     VARCHAR(120),
    contacto     VARCHAR(120)
);

ALTER TABLE proveedores ADD COLUMN IF NOT EXISTS producto VARCHAR(120);
ALTER TABLE proveedores ADD COLUMN IF NOT EXISTS contacto VARCHAR(120);

UPDATE proveedores
SET producto = COALESCE(producto, 'Servicios y suministros'),
    contacto = COALESCE(contacto, correo)
WHERE producto IS NULL OR contacto IS NULL;

CREATE TABLE IF NOT EXISTS productos (
    id_producto  SERIAL PRIMARY KEY,
    nombre       VARCHAR(100) NOT NULL,
    categoria    VARCHAR(50) NOT NULL,
    precio       NUMERIC(10,2) NOT NULL CHECK (precio >= 0),
    stock        INTEGER CHECK (stock IS NULL OR stock >= 0),
    id_proveedor INTEGER REFERENCES proveedores(id_proveedor) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS clientes (
    id_cliente SERIAL PRIMARY KEY,
    nombre     VARCHAR(100) NOT NULL,
    cedula     VARCHAR(20),
    telefono   VARCHAR(20),
    correo     VARCHAR(120),
    empresa    VARCHAR(120),
    activo     BOOLEAN NOT NULL DEFAULT TRUE
);

ALTER TABLE clientes ADD COLUMN IF NOT EXISTS empresa VARCHAR(120);
ALTER TABLE clientes ADD COLUMN IF NOT EXISTS activo BOOLEAN NOT NULL DEFAULT TRUE;

CREATE TABLE IF NOT EXISTS facturas (
    id_factura SERIAL PRIMARY KEY,
    id_cliente INTEGER REFERENCES clientes(id_cliente) ON DELETE SET NULL,
    fecha      DATE NOT NULL,
    total      NUMERIC(10,2) NOT NULL CHECK (total >= 0),
    numero     VARCHAR(30),
    estado     VARCHAR(30) NOT NULL DEFAULT 'Pendiente'
);

ALTER TABLE facturas ADD COLUMN IF NOT EXISTS numero VARCHAR(30);
ALTER TABLE facturas ADD COLUMN IF NOT EXISTS estado VARCHAR(30) NOT NULL DEFAULT 'Pendiente';

UPDATE facturas
SET numero = 'F-' || LPAD(id_factura::text, 3, '0')
WHERE numero IS NULL OR BTRIM(numero) = '';

CREATE UNIQUE INDEX IF NOT EXISTS uq_facturas_numero ON facturas(numero);

CREATE TABLE IF NOT EXISTS usuarios (
    id       SERIAL PRIMARY KEY,
    usuario  VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_productos_proveedor ON productos(id_proveedor);
CREATE INDEX IF NOT EXISTS idx_facturas_cliente ON facturas(id_cliente);
