from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.disciplina import Disciplina
from app.schemas.disciplina import DisciplinaCreate, DisciplinaUpdate


def crear_disciplina(db: Session, data: DisciplinaCreate):
    existe = db.query(Disciplina).filter(Disciplina.nombre == data.nombre).first()
    if existe:
        raise HTTPException(409, f"La disciplina '{data.nombre}' ya existe")
    disciplina = Disciplina(**data.model_dump())
    db.add(disciplina)
    db.commit()
    db.refresh(disciplina)
    return disciplina


def listar_disciplinas(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Disciplina).offset(skip).limit(limit).all()


def obtener_disciplina(db: Session, disciplina_id: int):
    disciplina = db.query(Disciplina).filter(Disciplina.id == disciplina_id).first()
    if not disciplina:
        raise HTTPException(404, "Disciplina no encontrada")
    return disciplina


def actualizar_disciplina(db: Session, disciplina_id: int, data: DisciplinaUpdate):
    disciplina = db.query(Disciplina).filter(Disciplina.id == disciplina_id).first()
    if not disciplina:
        raise HTTPException(404, "Disciplina no encontrada")
    for campo, valor in data.model_dump(exclude_unset=True).items():
        setattr(disciplina, campo, valor)
    db.commit()
    db.refresh(disciplina)
    return disciplina