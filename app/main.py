from fastapi import FastAPI
from app.database import Base, engine
from app.routes import auth_router, profile_router, views_router, patient_router
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# Create all tables (for development, in production use migrations)
Base.metadata.create_all(bind=engine)

app.include_router(auth_router)
app.include_router(profile_router)
app.include_router(views_router)
app.include_router(patient_router)

# Serve static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.get("/")
def read_root():
    return {"message": "AMS API is running"} 