import pytest
from uuid import uuid4

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker, scoped_session
from sqlalchemy.orm.session import close_all_sessions
from sqlalchemy.exc import SQLAlchemyError

from app.database import Base, get_db
from app.main import app

import os

APP_ENV = os.environ.get('APP_ENV')

DB_USER = os.environ.get('MYSQL_USER')
DB_PASSWORD = os.environ.get('MYSQL_PASSWORD')
DB_HOST = os.environ.get('MYSQL_HOST')
DB_NAME = os.environ.get('MYSQL_DATABASE')

# テスト用のセッションクラスを作成する
class TestingSession(Session):
 def commit(self):
     self.flush()
     self.expire_all()
     
@pytest.fixture(scope="function")
def test_db():
    DATABASE = 'mysql://%s:%s@%s/%s?charset=utf8' % (
    DB_USER,
    DB_PASSWORD,
    DB_HOST,
    DB_NAME,
)
    engine = create_engine(DATABASE,encoding='utf-8',echo=True)
    Base.metadata.create_all(bind=engine)

    function_scope = uuid4().hex
    TestingSessionLocal = scoped_session(
        sessionmaker(
            class_=TestingSession,
            autocommit=False,
            autoflush=False,
            bind=engine
        ),
        scopefunc=lambda: function_scope,
    )
    Base.query = TestingSessionLocal
    
    def get_db_for_testing():
      db = TestingSessionLocal()
      try:
          yield db
          db.commit()
      except SQLAlchemyError:
          db.rollback()

#   　テスト時に依存するDBを本番用からテスト用のものに切り替える 
    app.dependency_overrides[get_db] = get_db_for_testing
    yield TestingSessionLocal()
    Base.metadata.drop_all(bind=engine) 
    close_all_sessions()
    # セッション終了後にengineを破棄し、DBの状態を初期化する
    engine.dispose()