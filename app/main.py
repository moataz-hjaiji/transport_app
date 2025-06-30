from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database.database import engine, Base
from app.models.user import User
from app.routes.user import router as user_router
from app.routes.admin import router as admin_router
from app.routes.stations import router as stations_router
from app.middleware.log_requests import log_requests

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.middleware("http")(log_requests)
# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(user_router, prefix="/api/auth", tags=["auth"])
app.include_router(admin_router)
app.include_router(stations_router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI authentication system"}