from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.api.v1.routers import api_router 

app = FastAPI(
    title="Mission OAuth SaaS API",
    version="1.0.0",
    description="FastAPI + Google OAuth + Postgres backend",
    docs_url="/docs" if settings.ENVIRONMENT == "development" else None,
    redoc_url="/redoc" if settings.ENVIRONMENT == "development" else None,
)

# ── CORS ───────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Include all v1 routes ──────────────────────────────
app.include_router(api_router, prefix="/api/v1")

# ── Health check ───────────────────────────────────────
@app.get("/health", tags=["System"])
def health_check():
    return {"status": "ok", "service": "Mission OAuth SaaS API"}