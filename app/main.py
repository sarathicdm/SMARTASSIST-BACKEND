from fastapi import FastAPI
from app.routers import health, users
from app.database import engine, Base
from app.routers import auth

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="SmartAssist Backend")

app.include_router(health.router)
app.include_router(users.router)
app.include_router(auth.router)


@app.get("/")
def root():
    return {"message": "Backend is running successfully 🚀"}
