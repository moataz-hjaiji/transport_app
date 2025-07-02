from  app.admin.routes import api_router as admin_router
from app.user.router import router as user_router


all_routers = [
    admin_router,
    user_router,
]
