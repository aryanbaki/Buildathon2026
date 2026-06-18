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
    from backend.auth_status import verify_anthropic_key, tavily_configured, use_demo_mode

    anthropic = verify_anthropic_key()
    return {
        "status": "ok" if health_check() else "degraded",
        "db": health_check(),
        "anthropic": anthropic,
        "tavily": {"ok": tavily_configured()},
        "demo_mode": use_demo_mode(),
    }
