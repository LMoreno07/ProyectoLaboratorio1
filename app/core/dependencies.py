from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.models.database import get_db
from app.models.usuario import Usuario
from app.core.security import decodificar_token

security = HTTPBearer()  #OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),#token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
    ) -> Usuario:
    ##
    from app.core.config import settings
    print("🔑 SECRET_KEY al decodificador:", settings.SECRET_KEY)  # ← DEBUG
    ##

    token = credentials.credentials  # Extrae el token sin el Bearer
    print(f"Token recibido {token[:20]} ...")
    payload = decodificar_token(token)
    print(f"Payload recibido {payload} ...")
    if not payload:
        raise HTTPException(status_code=401, detail="Token inválido o expirado")
    
    usuario = db.query(Usuario).filter(Usuario.id == int(payload.get("sub"))).first()
    if not usuario or not usuario.activo:
        raise HTTPException(status_code=401, detail="Usuario no encontrado o inactivo")
    return usuario

def require_role(rol_nombre: str):
    def role_checker(current_user: Usuario = Depends(get_current_user)):
        if current_user.rol.nombre != rol_nombre:
            raise HTTPException(status_code=403, detail=f"Se requiere rol: {rol_nombre}")
        return current_user
    return role_checker