from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.categoria_maquina import CategoriaMaquina
from app.schemas.categoria_maquina import CategoriaMaquinaCreate, CategoriaMaquinaUpdate

def crear_categoria(db: Session, categoria: CategoriaMaquinaCreate):
    existe = db.query(CategoriaMaquina).filter(CategoriaMaquina.nombre.ilike(categoria.nombre)).first()
    if existe:
        raise HTTPException(status_code=400, detail="Esta categoría ya existe")
    
    nueva = CategoriaMaquina(**categoria.model_dump())
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return nueva

def listar_categorias(db: Session, skip: int = 0, limit: int = 10):
    return db.query(CategoriaMaquina).offset(skip).limit(limit).all()

def obtener_categoria(db: Session, categoria_id: int):
    """Obtener categoría por ID."""
    categoria = db.query(CategoriaMaquina).filter(CategoriaMaquina.id == categoria_id).first()
    if not categoria:
        raise HTTPException(404, "Categoría no encontrada")
    return categoria

def actualizar_categoria(db: Session, categoria_id: int, data: CategoriaMaquinaUpdate):
    """Actualizar categoría. Solo Admin."""
    categoria = db.query(CategoriaMaquina).filter(CategoriaMaquina.id == categoria_id).first()
    if not categoria:
        raise HTTPException(404, "Categoría no encontrada")
    for campo, valor in data.model_dump(exclude_unset=True).items():
        setattr(categoria, campo, valor)
    db.commit()
    db.refresh(categoria)
    return categoria