from fastapi import APIRouter

from .user import router as  user_router
from .admin import router as  admin_router
from .stations import router as  stations_router
from .driver import router as driver_router


api_router = APIRouter(prefix='/admins')

api_router.include_router(user_router)
api_router.include_router(admin_router)
api_router.include_router(stations_router)
api_router.include_router(driver_router)


routers = [
    (user_router, "/api/auth", ["auth"]),
    (admin_router, "", []),
    (stations_router, "", []),
    (driver_router,'',[])
]
