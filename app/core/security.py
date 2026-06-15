from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verificar_password(password_plano: str, password_hash: str) -> bool:
    """Compara una contraseña en texto plano con su hash"""
    return pwd_context.verify(password_plano, password_hash)

def hashear_password(password: str) -> str:
    """Genera el hash de una contraseña"""
    return pwd_context.hash(password)

def crear_token_acceso(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Genera un token JWT con los datos proporcionados"""
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

#def decodificar_token(token: str) -> Optional[dict]:
#    """Decodifica y valida un token JWT"""
#    try:
#        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
#        return payload
#    except JWTError:
#        return None

def decodificar_token(token: str) -> Optional[dict]:
    """Decodifica y valida un token JWT"""
    from jose import jwt, JWTError
    from app.core.config import settings
    try:
        payload = jwt.decode(
            token, 
            settings.SECRET_KEY, 
            algorithms=[settings.ALGORITHM],
            options={"verify_exp": True}
        )
        return payload
    
    except jwt.ExpiredSignatureError:
        # El token exiro.
        print("El token ha caducado!")
        return None
    except jwt.InvalidTokenError:
        # El token es falso, mal copiado o roto
        print("El token es invalido!")
        return None
    #except JWTError as e:
    #    print(f"❌ Error JWT: {e}")
    #    return None
    #except Exception as e:
    #    print(f"❌ Error inesperado: {e}")
    #    return None