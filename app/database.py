from sqlalchemy import create_engine,types
from sqlalchemy.orm import sessionmaker, scoped_session, DeclarativeBase
from .env import DB_USER, DB_PASSWORD, DB_HOST, DB_NAME
import uuid
DATABASE = "postgresql://%s:5432/%s?user=%s&password=%s" % (
    DB_HOST,
    DB_NAME,
    DB_USER,
    DB_PASSWORD,
)

engine = create_engine(
    DATABASE,
    echo=True
)

# 実際の DB セッション
SessionLocal = scoped_session(
    sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine
    )
)

class Base(DeclarativeBase):
    pass
Base.query = SessionLocal.query_property()


# Dependency Injection用
def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()