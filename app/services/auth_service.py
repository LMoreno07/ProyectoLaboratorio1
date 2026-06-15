from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.usuario import Usuario
from app.core.security import verificar_password, crear_token_acceso


def autenticar_usuario(db: Session, email: str, password: str):
    usuario = db.query(Usuario).filter(Usuario.email == email).first()

    if not usuario:
        raise HTTPException(401, "Email o contraseña incorrectos")
   
    if not verificar_password(password, usuario.password_hash):
        raise HTTPException(401, "Email o contraseña incorrectos")
   
    if not usuario.activo:
        raise HTTPException(403, "Usuario inactivo")
   
    token = crear_token_acceso({"sub": str(usuario.id)})
   
    return {
        "access_token": token,
        "token_type": "bearer",
        "usuario_id": usuario.id,
        "email": usuario.email,
        "rol": usuario.rol.nombre
    }