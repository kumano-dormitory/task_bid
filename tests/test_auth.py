from fastapi.testclient import TestClient
from app.main import app

client=TestClient(app)

user={
        "name":"testUser",
        "password":"testUserPassword",
        "block":"B3",
        "room_numnber":"B310"
    }

def test_sign_up():
    
    response=client.post("/register/",json=user)
    assert response.status_code == 200
    response_user=client.post("/login",data={
        "name":"testUser",
        "password":"testUserPassword"
    })
    access_token=response.json().get("access_token")
    assert access_token
    response_get=client.get("/users/"+response_user.id,headers={
        "Authorization":f'Bearer {access_token}'
    })
    assert response_get.status_code==200
    assert response_get.json().get("name")=="testUser"
    assert response_get.json().get("room_number")=="B310"
    

