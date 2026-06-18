"""
Teja — app.py
FastAPI entrypoint. Run with: uvicorn backend.app:app --reload --port 8000
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.api.routes import router
from backend.database.db import init_db

app = FastAPI(title="Fleet Document Intelligence", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup():
    init_db()


app.include_router(router)


@app.get("/health")
def health():
    from backend.database.db import health_check
    return {"status": "ok", "db": health_check()}
