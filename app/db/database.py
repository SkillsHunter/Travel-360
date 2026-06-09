from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

#DATABASE_URL = os.getenv("postgresql://neondb_owner:npg_VbgA4ZDzu7or@ep-young-morning-aoevy1fo-pooler.c-2.ap-southeast-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require")
DATABASE_URL = os.getenv("postgresql://neondb_owner:npg_VbgA4ZDzu7or@ep-young-morning-aoevy1fo-pooler.c-2.ap-southeast-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is missing")

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=180,
    pool_size=5,
    max_overflow=10,
    connect_args={
        "sslmode": "require"
    }
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()


def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()
