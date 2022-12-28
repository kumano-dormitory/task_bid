from fastapi.testclient import TestClient
from app.main import app
from app.models.authority import Authority
from app.models.slot import TaskTag
from app.models.slot import Slot 
from app.models.users import User
from app.cruds.user import user_register,user_get

client=TestClient(app)

user={
        "name":"testUser",
        "password":"testUserPassword",
        "block":"B3",
        "room_numnber":"B310"
    }


def test_add_user():
    
    response=client.post("/register/",json=user)
    assert response.status_code == 200
    response=client.post("/login",data={
        "name":"testUser",
        "password":"testUserPassword"
    })
    access_token=response.json().get("access_token")
    assert access_token


def test_add_task():
    task={
        "name":"testtask",
        "detail":"This is the task json for testing (これはテスト用のTaskオブジェクトです)",
        "authority":[],
        "tag":[]
    }
    response=client.post("/tasks/",json=task)
    assert response.status_code == 200

def test_add_slot():
    users=client.get("/users/")
    firstUser=users[0]
    
    slot={
        "name":"testslot",
        "start_time_year":2022,
        "start_time_month":12,
        "start_time_day":30,
        "start_time_hour":22,
        "start_time_minute":0,
        "end_time_year":2022,
        "end_time_month":12,
        "end_time_day":31,
        "end_time_hour":8,
        "end_time_minute":0,
        "creater":testUser.id
        "task":
    }

    
    

{ "name":"testuser","password":"testpassword","block":"B3","room_number":"B310"}