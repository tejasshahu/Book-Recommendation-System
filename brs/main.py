from fastapi import FastAPI

from database import engine
from models import Base
from views import router

# Initialize FastAPI app
app = FastAPI()

# Create all database tables
Base.metadata.create_all(bind=engine)

# Include the router from views.py
app.include_router(router)
