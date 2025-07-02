from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database.database import engine, Base
from app.helper.seeder import seeder

from app.middleware.log_requests import log_requests
import asyncio
from app.routes import api_router


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
app.include_router(api_router)

try:
    loop = asyncio.get_running_loop()
    loop.create_task(seeder())
except RuntimeError:
    asyncio.run(seeder())
@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI authentication system"}


