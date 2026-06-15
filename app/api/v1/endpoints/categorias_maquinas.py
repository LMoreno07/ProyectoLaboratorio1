from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from app.models.database import get_db
from app.schemas.categoria_maquina import CategoriaMaquinaCreate, CategoriaMaquinaResponse, CategoriaMaquinaUpdate
from app.services import categoria_maquina_services
from app.models.usuario import Usuario
from app.core.dependencies import require_role, get_current_user

router = APIRouter(prefix="/categorias-maquinas", tags=["Máquinas"])

@router.post("/", response_model=CategoriaMaquinaResponse, status_code=201)
def crear_categoria(
    data: CategoriaMaquinaCreate, 
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_role("Administrador"))
    ):
    """Crear categoria de máquina"""
    return categoria_maquina_services.crear_categoria(db, data)

@router.get("/", response_model=List[CategoriaMaquinaResponse])
def listar_categorias(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
    ):
    """Listar categorias"""
    return categoria_maquina_services.listar_categorias(db, skip, limit)


@router.get("/{categoria_id}", response_model=CategoriaMaquinaResponse)
def obtener_categoria(
    categoria_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
    ):
    """Obtener categoria por ID"""
    return categoria_maquina_services.obtener_categoria(db, categoria_id)


@router.patch("/{categoria_id}", response_model=CategoriaMaquinaResponse)
def actualizar_categoria(
    categoria_id: int,
    data: CategoriaMaquinaUpdate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_role("Administrador"))
    ):
    """Actualizar categoría"""
    return categoria_maquina_services.actualizar_categoria(db, categoria_id, data)
