from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.models.database import get_db
from app.models.entrenador import Entrenador
from app.models.usuario import Usuario
from app.schemas.entrenador import EntrenadorCreate, EntrenadorUpdate, EntrenadorResponse

router = APIRouter(prefix="/entrenadores", tags=["Entrenadores"])

@router.post("/", response_model=EntrenadorResponse, status_code=201)
def crear_entrenador(datos: EntrenadorCreate, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.id == datos.usuario_id).first()
    if not usuario:
        raise HTTPException(404, "Usuario no encontrado")
    existe = db.query(Entrenador).filter(Entrenador.usuario_id == datos.usuario_id).first()
    if existe:
        raise HTTPException(409, "El usuario ya es entrenador")
    entrenador = Entrenador(**datos.model_dump())
    db.add(entrenador)
    db.commit()
    db.refresh(entrenador)
    return entrenador

@router.get("/", response_model=List[EntrenadorResponse])
def listar_entrenadores(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(Entrenador).offset(skip).limit(limit).all()

@router.get("/{entrenador_id}", response_model=EntrenadorResponse)
def obtener_entrenador(entrenador_id: int, db: Session = Depends(get_db)):
    entrenador = db.query(Entrenador).filter(Entrenador.id == entrenador_id).first()
    if not entrenador:
        raise HTTPException(404, "Entrenador no encontrado")
    return entrenador

@router.patch("/{entrenador_id}", response_model=EntrenadorResponse)
def actualizar_entrenador(entrenador_id: int, datos: EntrenadorUpdate, db: Session = Depends(get_db)):
    entrenador = db.query(Entrenador).filter(Entrenador.id == entrenador_id).first()
    if not entrenador:
        raise HTTPException(404, "Entrenador no encontrado")
    for campo, valor in datos.model_dump(exclude_unset=True).items():
        setattr(entrenador, campo, valor)
    db.commit()
    db.refresh(entrenador)
    return entrenador