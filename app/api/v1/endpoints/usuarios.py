from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.models.database import get_db
from app.models.usuario import Usuario
from app.models.rol import Rol
from app.schemas.usuario import UsuarioCreate, UsuarioResponse
from app.core.security import hashear_password
from app.core.dependencies import get_current_user, require_role  # Para proteger rutas

router = APIRouter(
    prefix="/usuarios",
    tags=["Usuarios"]
)

@router.post("/", response_model=UsuarioResponse, status_code=201)
def crear_usuario(
    usuario: UsuarioCreate, 
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_role("Administrador"))  # Solo admind puede crear
    ):
    """Registrar un nuevo usuario en el sistema"""
    # Verificar email único
    existe = db.query(Usuario).filter(Usuario.email == usuario.email).first()
    if existe:
        raise HTTPException(status_code=409, detail="El email ya está registrado")
    
    # Verificar que el rol existe
    rol = db.query(Rol).filter(Rol.id == usuario.rol_id).first()
    if not rol:
        raise HTTPException(status_code=404, detail="Rol no encontrado")
    
    # Crear usuario con contraseña hasheada
    nuevo_usuario = Usuario(
        email=usuario.email,
        password_hash=hashear_password(usuario.password),
        nombre=usuario.nombre,
        apellido=usuario.apellido,
        rol_id=usuario.rol_id
    )
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    return nuevo_usuario

@router.get("/", response_model=List[UsuarioResponse])
def listar_usuarios(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_role("Administrador"))  #  Solo para admin 
    ):
    """Listar usuarios con paginación"""
    return db.query(Usuario).offset(skip).limit(limit).all()

@router.get("/{usuario_id}", response_model=UsuarioResponse)
def obtener_usuario(
    usuario_id: int, 
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)  #  Cualquier Usuario autenticado
    ):
    """Obtener un usuario por su ID"""
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario

@router.patch("/{usuario_id}",response_model=UsuarioResponse)
def actualizar_usuario(
    usuario_id: int,
    usuario_update: UsuarioCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
    ):
    """
    Actualizar datos de un usuario.
    Solo el propio usuario y el admin pueden modificar laInformación 
    """
    usuario = db.query(Usuario).filter(Usuario.id==usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    # Verificar que sea el propio usuario o el admin
    if current_user.id != usuario_id and current_user.rol.nombre != "Administrador":
        raise HTTPException(status_code=403, detail="No tienes permiso para modificar este usuario")
    
    # Actualizar solo los campos enviados
    datos = usuario_update.model_dump(exclude_unset=True)
    if "password" in datos:
        datos["password_hash"] = hashear_password(datos.pop("password")) # Hashear si cambia la contraseña

    for campo, valor in datos.items():
        setattr(usuario, campo, valor)

    db.commit()
    db.refresh(usuario)
    return usuario
