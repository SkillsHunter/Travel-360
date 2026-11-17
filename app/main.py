import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.travel import router
from app.db.database import Base, engine

Base.metadata.create_all(bind=engine)

# Interactive API docs are off unless ENABLE_DOCS=1 is set.
# They list every endpoint, so keep them off in production.
ENABLE_DOCS = os.getenv("ENABLE_DOCS") == "1"

app = FastAPI(
    title="Travel-360",
    docs_url="/docs" if ENABLE_DOCS else None,
    redoc_url="/redoc" if ENABLE_DOCS else None,
    openapi_url="/openapi.json" if ENABLE_DOCS else None
)

# Comma-separated list of browser origins allowed to call the API.
# The Streamlit app calls the API server-side, so it needs no entry here.
ALLOWED_ORIGINS = [
    origin.strip()
    for origin in os.getenv("ALLOWED_ORIGINS", "").split(",")
    if origin.strip()
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_methods=["POST"],
    allow_headers=["Content-Type", "X-API-Key"]
)

app.include_router(router)
