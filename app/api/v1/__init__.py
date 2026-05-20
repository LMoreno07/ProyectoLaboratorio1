"""
Centralizando todos los routers
"""

from app.api.v1.endpoints.deportivo import router as sesiones
from app.api.v1.endpoints import mantenimiento
from fastapi import APIRouter

from app.api.v1.endpoints import roles, usuarios, auth, maquinas, categorias_maquinas, reservas, clientes, entrenadores
    #acceso,
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
api_router.include_router(maquinas.router, tags=["Máquinas"])
api_router.include_router(categorias_maquinas.router, tags=["Categorías de Máquinas"])
api_router.include_router(mantenimiento.router, tags=["Mantenimiento"])
api_router.include_router(sesiones, tags=["Deportivo"])
api_router.include_router(reservas.router, tags=["Reservas"])
api_router.include_router(clientes.router, tags=["Clientes"])
api_router.include_router(entrenadores.router, tags=["Entrenadores"])
#api_router.include_router(acceso.router, tags=["Acceso"])
#api_router.include_router(finanzas.router, tags=["Finanzas"])
#api_router.include_router(tienda.router, tags=["Tienda"])
#pi_router.include_router(biometrico.router, tags=["Biométrico"])