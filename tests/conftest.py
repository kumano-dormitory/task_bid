import pytest
import typing
import httpx
from starlette.types import ASGIApp
from uuid import uuid4
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker, scoped_session
from sqlalchemy.orm.session import close_all_sessions
from sqlalchemy.exc import SQLAlchemyError
from app.database import Base, get_db
from app.main import app
import os

_RequestData = typing.Mapping[str, typing.Union[str, typing.Iterable[str]]]

APP_ENV = os.environ.get('APP_ENV')

DB_USER = os.environ.get('POSTGRES_USER')
DB_PASSWORD = os.environ.get('POSTGRES_PASSWORD')
DB_NAME = os.environ.get('POSTGRES_DB')

client=TestClient(app)

testUser={
        "name":"test_user",
        "password":"testUserPassword",
        "block":"B3",
        "room_number":"B310"
}
testUser2={
    "name":"test_user_2",
    "password":"testUser2Password",
    "block":"B3",
    "room_number":"B310"
}

class MyTestClient(TestClient):
    def __init__(self, app: ASGIApp,base_url: str = "http://testserver", 
                 raise_server_exceptions: bool = True, 
                 root_path: str = "", backend: str = "asyncio", 
                 backend_options: typing.Optional[typing.Dict[str, typing.Any]] = None, 
                 cookies = None) -> None:
       super().__init__(app, base_url, raise_server_exceptions, root_path, backend, backend_options, cookies)
       response=super().post("/register/",json=testUser)
       self.user=response.json()
       response2=super().post("/register/",json=testUser2)
       self.user2=response2.json()
       self.access_token=super().post("/login",data={
        "username":"test_user",
        "password":"testUserPassword"
        }).json().get("access_token")
       self.access_token_2=super().post("/login",data={
        "username":"test_user_2",
        "password":"testUser2Password"
       }).json().get("access_token")
       print(self.access_token,"conftest.py")
       
       
    def get(self, url: httpx._types.URLTypes, *, params: typing.Optional[httpx._types.QueryParamTypes] = None, 
            cookies: typing.Optional[httpx._types.CookieTypes] = None, 
            auth: typing.Union[httpx._types.AuthTypes, httpx._client.UseClientDefault] = httpx._client.USE_CLIENT_DEFAULT, 
            follow_redirects: typing.Optional[bool] = None, 
            allow_redirects: typing.Optional[bool] = None, 
            timeout = httpx._client.USE_CLIENT_DEFAULT, extensions: typing.Optional[typing.Dict[str, typing.Any]] = None) -> httpx.Response:
       return super().get(url, params=params, 
                          headers={"Authorization":f'Bearer {self.access_token}'}, 
                          cookies=cookies, 
                          auth=auth, 
                          follow_redirects=follow_redirects, 
                          allow_redirects=allow_redirects, 
                          timeout=timeout, extensions=extensions)
       
    def post(self, url: httpx._types.URLTypes, *, 
             content: typing.Optional[httpx._types.RequestContent] = None, 
             data: typing.Optional[_RequestData] = None, 
             files: typing.Optional[httpx._types.RequestFiles] = None, 
             json: typing.Any = None, params: typing.Optional[httpx._types.QueryParamTypes] = None, 
             headers: typing.Optional[httpx._types.HeaderTypes] = None,
             cookies: typing.Optional[httpx._types.CookieTypes] = None, 
             auth: typing.Union[httpx._types.AuthTypes, httpx._client.UseClientDefault] = httpx._client.USE_CLIENT_DEFAULT, 
             follow_redirects: typing.Optional[bool] = None, 
             allow_redirects: typing.Optional[bool] = None, 
             timeout = httpx._client.USE_CLIENT_DEFAULT, extensions: typing.Optional[typing.Dict[str, typing.Any]] = None) -> httpx.Response:
        if not headers:
            headers={"Authorization":f'Bearer {self.access_token}'}
        return super().post(url, content=content, data=data, files=files, json=json, params=params, 
                           headers=headers, 
                           cookies=cookies, auth=auth, follow_redirects=follow_redirects, 
                           allow_redirects=allow_redirects, timeout=timeout, extensions=extensions)

# テスト用のセッションクラスを作成する
class TestingSession(Session):
 def commit(self):
     self.flush()
     self.expire_all()
     
@pytest.fixture(scope="session",autouse=True)
def test_db():
    print("test_db_called")
    DATABASE = "postgresql+psycopg2://%s:%s@testdb:5432/%s" % (
    DB_USER,
    DB_PASSWORD,
    DB_NAME,)
    print(DATABASE,"データベース")
    engine = create_engine(DATABASE,echo=False)
    Base.metadata.drop_all(bind=engine) 
    Base.metadata.create_all(bind=engine)
    print("create_all_executed")

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
    Base.query = TestingSessionLocal.query_property()
    
    def get_db_for_testing():
      db = TestingSessionLocal()
      print("called get_test_db")
      try:
          yield db
          db.commit()
      except SQLAlchemyError:
          db.rollback()

#   　テスト時に依存するDBを本番用からテスト用のものに切り替える 
    app.dependency_overrides[get_db] = get_db_for_testing
    yield TestingSessionLocal()
    close_all_sessions()
    # セッション終了後にengineを破棄し、DBの状態を初期化する
    engine.dispose()
    

    
@pytest.fixture(scope="session")
def test_client():
    myclient=MyTestClient(app)
    yield myclient
    myclient.delete("/users/?name=test_user")
    
    