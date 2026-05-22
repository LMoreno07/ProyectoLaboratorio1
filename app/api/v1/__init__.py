"""
Centralizando todos los routers
"""

from app.api.v1.endpoints.sesiones import router as sesiones_router
from app.api.v1.endpoints.maquinas import router as maquinas_router
from app.api.v1.endpoints import mantenimiento
from fastapi import APIRouter

from app.api.v1.endpoints import roles, biometrico, usuarios, auth, ventas, disciplinas, productos,planes,categorias_maquinas, reservas, clientes, pagos, entrenadores, membresias,acceso
    #finanzas,
    #tienda,
    #biometrico
    #biometrico
#)

#Router principal para agrupar todos los modulos
api_router = APIRouter()

# Incluimos cada módulo con su prefijo
api_router.include_router(roles.router,tags=["Roles"])
api_router.include_router(usuarios.router, tags=["Usuarios"])
api_router.include_router(auth.router, tags=["Autenticación"])
api_router.include_router(maquinas_router, tags=["Máquinas"])
api_router.include_router(categorias_maquinas.router, tags=["Categorías de Máquinas"])
api_router.include_router(mantenimiento.router, tags=["Mantenimiento"])
api_router.include_router(sesiones_router, tags=["Deportivo"])
api_router.include_router(reservas.router, tags=["Reservas"])
api_router.include_router(clientes.router, tags=["Clientes"])
api_router.include_router(entrenadores.router, tags=["Entrenadores"])
api_router.include_router(pagos.router, tags=["Finanzas"])
api_router.include_router(membresias.router, tags=["Finanzas"])
api_router.include_router(disciplinas.router, tags=["Deportivo"])
api_router.include_router(planes.router, tags=["Finanzas"])
api_router.include_router(acceso.router, tags=["Acceso"])
#api_router.include_router(finanzas.router, tags=["Finanzas"])
#api_router.include_router(tienda.router, tags=["Tienda"])
api_router.include_router(productos.router, tags=["Tienda"])
api_router.include_router(ventas.router, tags=["Tienda"])
api_router.include_router(biometrico.router, tags=["Biométrico"])