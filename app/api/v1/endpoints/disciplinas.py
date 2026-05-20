from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.models.database import get_db
from app.models.disciplina import Disciplina
from app.schemas.disciplina import DisciplinaCreate, DisciplinaUpdate, DisciplinaResponse

router = APIRouter(prefix="/disciplinas", tags=["Deportivo"])


@router.post("/", response_model=DisciplinaResponse, status_code=201)
def crear_disciplina(datos: DisciplinaCreate, db: Session = Depends(get_db)):
    existe = db.query(Disciplina).filter(Disciplina.nombre == datos.nombre).first()
    if existe:
        raise HTTPException(409, f"La disciplina '{datos.nombre}' ya existe")
    disciplina = Disciplina(**datos.model_dump())
    db.add(disciplina)
    db.commit()
    db.refresh(disciplina)
    return disciplina


@router.get("/", response_model=List[DisciplinaResponse])
def listar_disciplinas(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(Disciplina).offset(skip).limit(limit).all()


@router.get("/{disciplina_id}", response_model=DisciplinaResponse)
def obtener_disciplina(disciplina_id: int, db: Session = Depends(get_db)):
    disciplina = db.query(Disciplina).filter(Disciplina.id == disciplina_id).first()
    if not disciplina:
        raise HTTPException(404, "Disciplina no encontrada")
    return disciplina


@router.patch("/{disciplina_id}", response_model=DisciplinaResponse)
def actualizar_disciplina(disciplina_id: int, datos: DisciplinaUpdate, db: Session = Depends(get_db)):
    disciplina = db.query(Disciplina).filter(Disciplina.id == disciplina_id).first()
    if not disciplina:
        raise HTTPException(404, "Disciplina no encontrada")
    for campo, valor in datos.model_dump(exclude_unset=True).items():
        setattr(disciplina, campo, valor)
    db.commit()
    db.refresh(disciplina)
    return disciplina