# CSi - CoFre Sistemas Informáticos (Semana 14 - Login funcional)

## Novedades de esta semana
Se incorporó un **sistema de autenticación completo** con **Flask-Login**
y **Werkzeug**, integrado con la base de datos PostgreSQL de la Semana 13.

- **Tabla `usuarios`** agregada a `sql/esquema.sql` (`id`, `usuario`
  UNIQUE, `password`). La contraseña **nunca** se guarda en texto plano:
  siempre se transforma con `generate_password_hash()` antes del INSERT.
- **`models.py`**: clase `Usuario(UserMixin)` — el modelo que Flask-Login
  necesita, con `obtener_por_id()` (para `load_user`) y
  `obtener_por_nombre_usuario()` (para el login).
- **`forms/login_form.py`** y **`forms/usuario_form.py`** (Flask-WTF),
  agregados al `forms/__init__.py` centralizado.
- **`LoginManager`** configurado en `app.py`, con `login_view='login'`
  (redirige automáticamente ahí a cualquiera que intente entrar a una
  página protegida sin sesión) y `user_loader` (`load_user`).
- **Rutas nuevas**:
  - `/registro` (GET/POST): registra un usuario nuevo. Si el nombre ya
    existe, la restricción `UNIQUE` de PostgreSQL lo rechaza y se muestra
    un mensaje claro (sin romper con un error 500).
  - `/login` (GET/POST): busca el usuario con `SELECT`, y compara la
    contraseña con `check_password_hash()` — **nunca** comparando el
    texto plano contra el hash directamente. Si es correcto, llama a
    `login_user()`.
  - `/logout`: llama a `logout_user()` y redirige al login.
  - `/dashboard`: panel protegido, punto de entrada a los módulos.
- **`@login_required`** en **todas** las rutas de administración:
  `/productos`, `/productos/nuevo`, `/productos/editar/<id>`,
  `/productos/eliminar/<id>`, y lo mismo para clientes, proveedores y
  facturación. Escribir la URL directamente sin sesión redirige al login.
- **`current_user`** se usa en el navbar (muestra el nombre del usuario
  autenticado y el enlace "Cerrar sesión") y en `dashboard.html`
  ("Bienvenido, `{{ current_user.usuario }}`").
- **Buenas prácticas de configuración** (adoptadas también en el proyecto
  de referencia de la compañera Marjorie Granda): `python-dotenv` +
  `.env.example` + `.gitignore`, para que ni la `SECRET_KEY` ni las
  credenciales de PostgreSQL queden hardcodeadas ni se suban al
  repositorio. También se agregó `crear_base_datos_si_no_existe()` en
  `conexion/conexion.py`, que crea la base de datos automáticamente si
  todavía no existe (basta con tener PostgreSQL instalado).
- `forms/__init__.py` ahora centraliza todos los imports de formularios
  (`from forms import ProductoForm, ..., LoginForm, UsuarioForm`).

## Estructura
```
csi-flask/
├── index.html            <- ORIGINAL sin cambios, es el que usa GitHub Pages
├── script.js              <- ORIGINAL sin cambios
├── app.py
├── models.py                <- NUEVO (Semana 14)
├── requirements.txt
├── .env.example              <- NUEVO (Semana 14)
├── .gitignore                <- NUEVO (Semana 14)
├── conexion/
│   ├── __init__.py
│   └── conexion.py             (+ python-dotenv, crear_base_datos_si_no_existe)
├── sql/
│   └── esquema.sql             (+ tabla usuarios)
├── forms/
│   ├── __init__.py              (centraliza todos los imports)
│   ├── login_form.py           <- NUEVO
│   ├── usuario_form.py         <- NUEVO
│   ├── producto_form.py
│   ├── cliente_form.py
│   ├── proveedor_form.py
│   └── facturacion_form.py
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── login.html              <- NUEVO
│   ├── registro.html           <- NUEVO
│   ├── dashboard.html          <- NUEVO
│   ├── productos.html
│   ├── formulario_producto.html
│   ├── clientes.html
│   ├── formulario_cliente.html
│   ├── proveedores.html
│   ├── formulario_proveedor.html
│   ├── facturacion.html
│   ├── formulario_facturacion.html
│   └── components/
│       ├── navbar.html            (+ estado de sesión / Cerrar sesión)
│       └── footer.html
└── static/
    ├── css/style.css
    ├── js/script.js
    └── img/
```

**Importante:** GitHub Pages solo sirve archivos estáticos. Todo el
sistema de login (`models.py`, `LoginManager`, las rutas nuevas) solo se
ejecuta localmente con `python app.py`.

## Configurar el entorno local
1. Copia `.env.example` como `.env` y ajusta los valores si tu instalación
   de PostgreSQL usa otro usuario/clave/nombre de base de datos:
   ```
   cp .env.example .env
   ```
   `.env` **no se sube** al repositorio (está en `.gitignore`) — ahí es
   donde irían credenciales reales en un entorno de verdad.
2. Instala las dependencias:
   ```
   pip install -r requirements.txt
   ```
3. Ejecuta la aplicación. Si la base de datos indicada en `.env` todavía
   no existe, `app.py` la crea sola (además de las tablas):
   ```
   python app.py
   ```

## Probar localmente el flujo completo de login
1. Abre http://127.0.0.1:5000/productos **sin haber iniciado sesión** →
   debes ser redirigido automáticamente a `/login` con un mensaje
   ("Por favor inicia sesión para acceder a esta página").
2. Ve a **"Regístrate aquí"**, crea un usuario (ej. `admin` / `Admin123`).
3. Verifica en PostgreSQL que el usuario quedó guardado y que la
   contraseña **no** es texto plano:
   ```
   psql -U csi_user -d csi_ferreteria -h localhost -c "SELECT * FROM usuarios;"
   ```
4. Intenta iniciar sesión con una contraseña **incorrecta** → debe
   rechazarse con "Usuario o contraseña incorrectos.".
5. Inicia sesión con la contraseña correcta → deberías llegar al
   **Dashboard**, con tu nombre de usuario visible en el navbar.
6. Entra a Productos, Clientes, Proveedores y Facturación — deben seguir
   funcionando exactamente igual que en la Semana 13 (CRUD completo en
   Productos contra PostgreSQL).
7. Clic en **"Cerrar sesión"**.
8. Intenta volver a escribir directamente `http://127.0.0.1:5000/productos`
   en la barra de direcciones → debe redirigirte de nuevo al login.
9. (Opcional) Reinicia Flask (Ctrl+C y `python app.py` de nuevo) y repite
   el login con el mismo usuario: debe seguir funcionando, porque el
   usuario vive en PostgreSQL, no en memoria.

## Subir a GitHub (flujo GUI, sin terminal)
1. No toques el `index.html` ni el `script.js` de la raíz (los usa GitHub
   Pages) — déjalos tal cual.
2. Reemplaza `app.py` y `requirements.txt`. Sube `models.py`,
   `.env.example` y `.gitignore` a la raíz del repositorio.
3. Reemplaza `conexion/conexion.py` y `forms/__init__.py`. Sube
   `forms/login_form.py` y `forms/usuario_form.py`.
4. Reemplaza `sql/esquema.sql` (ahora incluye la tabla `usuarios`).
5. Dentro de `templates`, sube `login.html`, `registro.html` y
   `dashboard.html`, y reemplaza `components/navbar.html`.
6. El resto de plantillas, formularios y estáticos **no cambiaron** esta
   semana.
7. **Nunca subas un archivo `.env` real** con contraseñas — solo
   `.env.example` (sin valores sensibles) va al repositorio.
8. Ejecuta `python app.py` localmente y repite la prueba obligatoria
   completa (registrar → verificar hash en la BD → login incorrecto
   rechazado → login correcto → acceder a ruta protegida → logout →
   intentar volver a acceder) antes de dar por terminado el avance.

## Nota sobre cuántos archivos subir
Si tu plataforma limita la cantidad de archivos por entrega, para esta
semana **basta con subir los que realmente cambiaron o son nuevos**:
- `app.py`
- `models.py`
- `requirements.txt`
- `.env.example`
- `.gitignore`
- `conexion/conexion.py`
- `sql/esquema.sql`
- `forms/__init__.py`
- `forms/login_form.py`
- `forms/usuario_form.py`
- `templates/login.html`
- `templates/registro.html`
- `templates/dashboard.html`
- `templates/components/navbar.html`

Todo lo demás (el resto de formularios, plantillas de productos/clientes/
proveedores/facturación y estáticos) es idéntico a lo entregado en la
Semana 13 y no necesita volver a subirse.
