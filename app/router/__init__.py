from  app.admin.routes import api_router as admin_router


all_routers = [
    (admin_router, "/admin"),
]
