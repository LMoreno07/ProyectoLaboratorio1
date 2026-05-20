from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.models.database import get_db
from app.models.venta_tienda import VentaTienda
from app.models.detalle_venta import DetalleVenta
from app.models.producto_tienda import ProductoTienda
from app.models.cliente import Cliente
from app.schemas.venta_tienda import VentaCreate, VentaResponse

router = APIRouter(prefix="/ventas", tags=["Tienda"])


@router.post("/", response_model=VentaResponse, status_code=201)
def registrar_venta(datos: VentaCreate, db: Session = Depends(get_db)):
    # Validar cliente si se proporciona
    if datos.cliente_id:
        if not db.query(Cliente).filter(Cliente.id == datos.cliente_id).first():
            raise HTTPException(404, "Cliente no encontrado")
    
    # Calcular total y validar stock
    total = 0
    for d in datos.detalles:
        producto = db.query(ProductoTienda).filter(ProductoTienda.id == d.producto_id).first()
        if not producto:
            raise HTTPException(404, f"Producto ID {d.producto_id} no encontrado")
        if producto.stock_actual < d.cantidad:
            raise HTTPException(409, f"Stock insuficiente para '{producto.nombre}'")
        total += d.cantidad * d.precio_unitario_aplicado
    
    # Crear venta
    venta = VentaTienda(
        cliente_id=datos.cliente_id,
        total=total,
        metodo_pago=datos.metodo_pago
    )
    db.add(venta)
    db.flush()  # Obtener venta.id sin hacer commit aún
    
    # Crear detalles y descontar stock
    for d in datos.detalles:
        subtotal = d.cantidad * d.precio_unitario_aplicado
        detalle = DetalleVenta(
            venta_id=venta.id,
            producto_id=d.producto_id,
            cantidad=d.cantidad,
            precio_unitario_aplicado=d.precio_unitario_aplicado,
            subtotal=subtotal
        )
        db.add(detalle)
        
        # Descontar stock
        producto = db.query(ProductoTienda).filter(ProductoTienda.id == d.producto_id).first()
        producto.stock_actual -= d.cantidad
    
    db.commit()
    db.refresh(venta)
    return venta


@router.get("/", response_model=List[VentaResponse])
def listar_ventas(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(VentaTienda).offset(skip).limit(limit).all()


@router.get("/{venta_id}", response_model=VentaResponse)
def obtener_venta(venta_id: int, db: Session = Depends(get_db)):
    venta = db.query(VentaTienda).filter(VentaTienda.id == venta_id).first()
    if not venta:
        raise HTTPException(404, "Venta no encontrada")
    return venta