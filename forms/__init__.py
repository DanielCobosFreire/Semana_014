# forms/__init__.py
# CSi - CoFre Sistemas Informáticos
# Semana 11: paquete "forms" que organiza las clases de formularios
# (Flask-WTF / WTForms) según los módulos de la aplicación.
# Semana 14: se centralizan los imports aquí (LoginForm y UsuarioForm
# incluidos), para que app.py pueda hacer simplemente
# "from forms import ProductoForm, ClienteForm, ..., LoginForm, UsuarioForm"
# en vez de una línea de import por archivo.

from .producto_form import ProductoForm
from .cliente_form import ClienteForm
from .proveedor_form import ProveedorForm
from .facturacion_form import FacturacionForm
from .login_form import LoginForm
from .usuario_form import UsuarioForm

__all__ = [
    'ProductoForm',
    'ClienteForm',
    'ProveedorForm',
    'FacturacionForm',
    'LoginForm',
    'UsuarioForm',
]
