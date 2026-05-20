from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.models.database import get_db
from app.models.producto_tienda import ProductoTienda
from app.schemas.producto_tienda import ProductoCreate, ProductoUpdate, ProductoResponse

router = APIRouter(prefix="/productos", tags=["Tienda"])


@router.post("/", response_model=ProductoResponse, status_code=201)
def crear_producto(datos: ProductoCreate, db: Session = Depends(get_db)):
    existe = db.query(ProductoTienda).filter(ProductoTienda.nombre == datos.nombre).first()
    if existe:
        raise HTTPException(409, f"El producto '{datos.nombre}' ya existe")
    producto = ProductoTienda(**datos.model_dump())
    db.add(producto)
    db.commit()
    db.refresh(producto)
    return producto


@router.get("/", response_model=List[ProductoResponse])
def listar_productos(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(ProductoTienda).offset(skip).limit(limit).all()


@router.get("/{producto_id}", response_model=ProductoResponse)
def obtener_producto(producto_id: int, db: Session = Depends(get_db)):
    producto = db.query(ProductoTienda).filter(ProductoTienda.id == producto_id).first()
    if not producto:
        raise HTTPException(404, "Producto no encontrado")
    return producto


@router.patch("/{producto_id}", response_model=ProductoResponse)
def actualizar_producto(producto_id: int, datos: ProductoUpdate, db: Session = Depends(get_db)):
    producto = db.query(ProductoTienda).filter(ProductoTienda.id == producto_id).first()
    if not producto:
        raise HTTPException(404, "Producto no encontrado")
    for campo, valor in datos.model_dump(exclude_unset=True).items():
        setattr(producto, campo, valor)
    db.commit()
    db.refresh(producto)
    return producto