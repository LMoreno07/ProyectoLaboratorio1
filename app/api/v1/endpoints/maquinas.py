from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.database import get_db
from app.models.maquina import Maquina
from app.models.categoria_maquina import CategoriaMaquina
from app.schemas.maquina import MaquinaCreate, MaquinaUpdate, MaquinaResponse

router = APIRouter(prefix="/maquinas", tags=["Máquinas"])


@router.post("/", response_model=MaquinaResponse, status_code=201)
def crear_maquina(data: MaquinaCreate, db: Session = Depends(get_db)):
    if not db.query(CategoriaMaquina).filter(CategoriaMaquina.id == data.categoria_id).first():
        raise HTTPException(404, "Categoría no encontrada")
    
    maquina = Maquina(**data.model_dump())
    db.add(maquina)
    db.commit()
    db.refresh(maquina)
    return maquina


@router.get("/", response_model=List[MaquinaResponse])
def listar_maquinas(
    skip: int = 0,
    limit: int = 10,
    categoria_id: Optional[int] = None,
    estado: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Maquina)
    if categoria_id:
        query = query.filter(Maquina.categoria_id == categoria_id)
    if estado:
        query = query.filter(Maquina.estado_operativo == estado)
    return query.offset(skip).limit(limit).all()


@router.get("/{maquina_id}", response_model=MaquinaResponse)
def obtener_maquina(maquina_id: int, db: Session = Depends(get_db)):
    maquina = db.query(Maquina).filter(Maquina.id == maquina_id).first()
    if not maquina:
        raise HTTPException(404, "Máquina no encontrada")
    return maquina


@router.patch("/{maquina_id}/estado", response_model=MaquinaResponse)
def cambiar_estado(maquina_id: int, estado: str, db: Session = Depends(get_db)):
    maquina = db.query(Maquina).filter(Maquina.id == maquina_id).first()
    if not maquina:
        raise HTTPException(404, "Máquina no encontrada")
    maquina.estado_operativo = estado
    db.commit()
    db.refresh(maquina)
    return maquina


@router.patch("/{maquina_id}", response_model=MaquinaResponse)
def actualizar_maquina(maquina_id: int, data: MaquinaUpdate, db: Session = Depends(get_db)):
    maquina = db.query(Maquina).filter(Maquina.id == maquina_id).first()
    if not maquina:
        raise HTTPException(404, "Máquina no encontrada")
    for campo, valor in data.model_dump(exclude_unset=True).items():
        setattr(maquina, campo, valor)
    db.commit()
    db.refresh(maquina)
    return maquina