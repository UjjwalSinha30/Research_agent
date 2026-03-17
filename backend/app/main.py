# backend/app/main.py

from fastapi import FastAPI
from app.api.routes import auth, agent
from app.db.init_db import init_db

app = FastAPI(title="Research Agent API")

@app.on_event("startup")
def startup():
    init_db()

app.include_router(auth.router)
app.include_router(agent.router)

@app.get("/health")
def health():
    return {"status": "ok"}
