from fastapi import FastAPI

from app.routes.travel import router
from app.db.database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Travel-360"
)

app.include_router(router)
