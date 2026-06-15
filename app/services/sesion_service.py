from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.sesion import Sesion
from app.models.disciplina import Disciplina
from app.models.entrenador import Entrenador
from app.schemas.sesion import SesionCreate, SesionUpdate


def crear_sesion(db: Session, data: SesionCreate):
    # Validar disciplina
    if not db.query(Disciplina).filter(Disciplina.id == data.disciplina_id).first():
        raise HTTPException(404, "Disciplina no encontrada")
    
    # Validar entrenador
    if not db.query(Entrenador).filter(Entrenador.id == data.entrenador_id).first():
        raise HTTPException(404, "Entrenador no encontrado")
    
    # Validar horario
    if data.hora_inicio >= data.hora_fin:
        raise HTTPException(409, "La hora de inicio debe ser menor a la de fin")
    
    # Validar solapamiento de entrenador
    conflicto = db.query(Sesion).filter(
        Sesion.entrenador_id == data.entrenador_id,
        Sesion.fecha == data.fecha,
        Sesion.hora_inicio < data.hora_fin,
        Sesion.hora_fin > data.hora_inicio
    ).first()
    if conflicto:
        raise HTTPException(409, "El entrenador ya tiene una sesión en ese horario")
    
    sesion = Sesion(**data.model_dump())
    db.add(sesion)
    db.commit()
    db.refresh(sesion)
    return sesion


def listar_sesiones(db: Session, skip: int = 0, limit: int = 10, fecha=None, disciplina_id: int = None):
    query = db.query(Sesion)
    if fecha:
        query = query.filter(Sesion.fecha == fecha)
    if disciplina_id:
        query = query.filter(Sesion.disciplina_id == disciplina_id)
    return query.offset(skip).limit(limit).all()


def obtener_sesion(db: Session, sesion_id: int):
    sesion = db.query(Sesion).filter(Sesion.id == sesion_id).first()
    if not sesion:
        raise HTTPException(404, "Sesión no encontrada")
    return sesion


def actualizar_sesion(db: Session, sesion_id: int, data: SesionUpdate):
    sesion = db.query(Sesion).filter(Sesion.id == sesion_id).first()
    if not sesion:
        raise HTTPException(404, "Sesión no encontrada")
    for campo, valor in data.model_dump(exclude_unset=True).items():
        setattr(sesion, campo, valor)
    db.commit()
    db.refresh(sesion)
    return sesion
