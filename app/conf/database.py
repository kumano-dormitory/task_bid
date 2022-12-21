from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# DB 接続情報
user_name = "user"
password = "password"
host = "db"
database_name = "sample_db"

# DB 接続設定
DATABASE_URL = 'mysql://%s:%s@%s/%s?charset=utf8mb4' % (
    user_name,
    password,
    host,
    database_name,
)

ENGINE = create_engine(
    DATABASE_URL,
    encoding="utf8",
    echo=True
)

# セッション設定
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=ENGINE
)

Base = declarative_base()