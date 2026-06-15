from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.maquina import Maquina
from app.models.categoria_maquina import CategoriaMaquina
from app.schemas.maquina import MaquinaCreate, MaquinaUpdate


def crear_maquina(db: Session, data: MaquinaCreate):
    # Validar que la categoría existe
    categoria = db.query(CategoriaMaquina).filter(CategoriaMaquina.id == data.categoria_id).first()
    if not categoria:
        raise HTTPException(404, "Categoría no encontrada")
    
    # Validar código serial único
    if data.codigo_serial:
        existe = db.query(Maquina).filter(Maquina.codigo_serial == data.codigo_serial).first()
        if existe:
            raise HTTPException(409, f"El código serial '{data.codigo_serial}' ya existe")
    
    maquina = Maquina(**data.model_dump())
    db.add(maquina)
    db.commit()
    db.refresh(maquina)
    return maquina


def listar_maquinas(db: Session, skip: int = 0, limit: int = 10, categoria_id: int = None, estado: str = None):
    query = db.query(Maquina)
    if categoria_id:
        query = query.filter(Maquina.categoria_id == categoria_id)
    if estado:
        query = query.filter(Maquina.estado_operativo == estado)
    return query.offset(skip).limit(limit).all()


def obtener_maquina(db: Session, maquina_id: int):
    maquina = db.query(Maquina).filter(Maquina.id == maquina_id).first()
    if not maquina:
        raise HTTPException(404, "Máquina no encontrada")
    return maquina


def cambiar_estado(db: Session, maquina_id: int, estado: str):
    maquina = db.query(Maquina).filter(Maquina.id == maquina_id).first()
    if not maquina:
        raise HTTPException(404, "Máquina no encontrada")
    maquina.estado_operativo = estado
    db.commit()
    db.refresh(maquina)
    return maquina


def actualizar_maquina(db: Session, maquina_id: int, data: MaquinaUpdate):
    maquina = db.query(Maquina).filter(Maquina.id == maquina_id).first()
    if not maquina:
        raise HTTPException(404, "Máquina no encontrada")
    
    # Validar código serial único si se actualiza
    if data.codigo_serial:
        existe = db.query(Maquina).filter(
            Maquina.codigo_serial == data.codigo_serial,
            Maquina.id != maquina_id
        ).first()
        if existe:
            raise HTTPException(409, f"El código serial '{data.codigo_serial}' ya existe")
    
    for campo, valor in data.model_dump(exclude_unset=True).items():
        setattr(maquina, campo, valor)
    db.commit()
    db.refresh(maquina)
    return maquina