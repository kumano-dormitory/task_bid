from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from env import DB_USER, DB_PASSWORD, DB_HOST, DB_NAME
from sqlalchemy.orm import sessionmaker, scoped_session
DATABASE = "mysql://%s:%s@%s/%s?charset=utf8" % (
    DB_USER,
    DB_PASSWORD,
    DB_HOST,
    DB_NAME,
)

engine = create_engine(DATABASE, encoding="utf-8", echo=True)

Base=declarative_base()

Session=scoped_session(sessionmaker(bind=engine))

