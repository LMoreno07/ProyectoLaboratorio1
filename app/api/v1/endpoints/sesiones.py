from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date
from app.models.database import get_db
from app.models.usuario import Usuario
from app.schemas.sesion import SesionCreate, SesionUpdate, SesionResponse
from app.services.sesion_service import (
    crear_sesion as _crear,
    listar_sesiones as _listar,
    obtener_sesion as _obtener,
    actualizar_sesion as _actualizar
)
from app.core.dependencies import get_current_user, require_role

router = APIRouter(prefix="/sesiones", tags=["Deportivo"])


@router.post("/", response_model=SesionResponse, status_code=201)
def crear_sesion(
    data: SesionCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_role("Administrador"))
):
    """Crear sesión."""
    return _crear(db, data)


@router.get("/", response_model=List[SesionResponse])
def listar_sesiones(
    skip: int = 0,
    limit: int = 10,
    fecha: Optional[date] = Query(None),
    disciplina_id: Optional[int] = Query(None),
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """Listar sesiones."""
    return _listar(db, skip, limit, fecha, disciplina_id)


@router.get("/{sesion_id}", response_model=SesionResponse)
def obtener_sesion(
    sesion_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """Obtener sesión."""
    return _obtener(db, sesion_id)


@router.patch("/{sesion_id}", response_model=SesionResponse)
def actualizar_sesion(
    sesion_id: int,
    data: SesionUpdate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_role("Administrador"))
):
    """Actualizar sesión."""
    return _actualizar(db, sesion_id, data)
