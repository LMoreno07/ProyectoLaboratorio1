from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.models.database import get_db
from app.models.usuario import Usuario
from app.schemas.disciplina import DisciplinaCreate, DisciplinaUpdate, DisciplinaResponse
from app.services.disciplina_services import (
    crear_disciplina as _crear,
    listar_disciplinas as _listar,
    obtener_disciplina as _obtener,
    actualizar_disciplina as _actualizar
)
from app.core.dependencies import get_current_user, require_role

router = APIRouter(prefix="/disciplinas", tags=["Deportivo"])


@router.post("/", response_model=DisciplinaResponse, status_code=201)
def crear_disciplina(
    data: DisciplinaCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_role("Administrador"))
):
    """Crear disciplina."""
    return _crear(db, data)


@router.get("/", response_model=List[DisciplinaResponse])
def listar_disciplinas(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """Listar disciplinas."""
    #print(f" Usuario: {current_user.email}, Rol: {current_user.rol.nombre}")  # DEBUG
    return _listar(db, skip, limit)


@router.get("/{disciplina_id}", response_model=DisciplinaResponse)
def obtener_disciplina(
    disciplina_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """Obtener disciplina."""
    return _obtener(db, disciplina_id)


@router.patch("/{disciplina_id}", response_model=DisciplinaResponse)
def actualizar_disciplina(
    disciplina_id: int,
    data: DisciplinaUpdate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_role("Administrador"))
):
    """Actualizar disciplina"""
    return _actualizar(db, disciplina_id, data)
