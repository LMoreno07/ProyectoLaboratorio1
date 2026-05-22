from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.categoria_maquina import CategoriaMaquina
from app.schemas.categoria_maquina import CategoriaMaquinaCreate

def crear_categoria(db: Session, categoria: CategoriaMaquinaCreate):
    db_categoria = db.query(CategoriaMaquina).filter(CategoriaMaquina.nombre.ilike(categoria.nombre)).first()
    if db_categoria:
        raise HTTPException(status_code=400, detail="Esta categoría ya existe")
    
    nueva = CategoriaMaquina(**categoria.dict())
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return nueva

def obtener_categorias(db: Session):
    return db.query(CategoriaMaquina).all()