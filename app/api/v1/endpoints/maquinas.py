from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.database import get_db
from app.models.usuario import Usuario
from app.schemas.maquina import MaquinaCreate, MaquinaUpdate, MaquinaResponse
from app.services.maquina_services import (
    crear_maquina as _crear,
    listar_maquinas as _listar,
    obtener_maquina as _obtener,
    cambiar_estado as _cambiar_estado,
    actualizar_maquina as _actualizar
)
from app.core.dependencies import get_current_user, require_role

router = APIRouter(prefix="/maquinas", tags=["Máquinas"])


@router.post("/", response_model=MaquinaResponse, status_code=201)
def crear_maquina(
    data: MaquinaCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_role("Administrador"))
):
    """Registrar máquina"""
    return _crear(db, data)


@router.get("/", response_model=List[MaquinaResponse])
def listar_maquinas(
    skip: int = 0,
    limit: int = 10,
    categoria_id: Optional[int] = None,
    estado: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """Listar máquinas"""
    return _listar(db, skip, limit, categoria_id, estado)


@router.get("/{maquina_id}", response_model=MaquinaResponse)
def obtener_maquina(
    maquina_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """Obtener máquina"""
    return _obtener(db, maquina_id)


@router.patch("/{maquina_id}/estado", response_model=MaquinaResponse)
def cambiar_estado(
    maquina_id: int,
    estado: str,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_role("Administrador"))
):
    """Cambiar estado operativo"""
    return _cambiar_estado(db, maquina_id, estado)


@router.patch("/{maquina_id}", response_model=MaquinaResponse)
def actualizar_maquina(
    maquina_id: int,
    data: MaquinaUpdate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_role("Administrador"))
):
    """Actualizar máquina"""
    return _actualizar(db, maquina_id, data)