from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session, DeclarativeBase
from .env import DB_USER, DB_PASSWORD, DB_HOST, DB_NAME

DATABASE = 'mysql://%s:%s@%s/%s?charset=utf8' % (
    DB_USER,
    DB_PASSWORD,
    DB_HOST,
    DB_NAME,
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
    print("get_db_called")
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()