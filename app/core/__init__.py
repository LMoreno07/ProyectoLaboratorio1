"""
Módulo core: Configuración y utilidades transversales
"""
from app.core.config import settings
from app.core.security import verificar_password, hashear_password, crear_token_acceso, decodificar_token
from app.core.dependencies import get_current_user, require_role