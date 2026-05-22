from sqlalchemy.orm import Session

from fastapi import HTTPException
from app.models.maquina import Maquina
from app.models.categoria_maquina import CategoriaMaquina
from app.schemas.maquina import MaquinaCreate

def crear_maquina(db: Session, maquina: MaquinaCreate):
    # Validar que la categoría exista
    cat = db.query(CategoriaMaquina).filter(CategoriaMaquina.id == maquina.categoria_id).first()
    if not cat:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    
    # Validar que no exista el serial
    existe = db.query(Maquina).filter(Maquina.codigo_serial == maquina.codigo_serial).first()
    if existe:
        raise HTTPException(status_code=400, detail="Ya existe una máquina con ese serial")
        
    nueva = Maquina(**maquina.dict())
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return nueva

def obtener_maquinas(db: Session):
    return db.query(Maquina).all()
