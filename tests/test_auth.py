from conftest import client

user={
        "name":"testUser",
        "password":"testUserPassword",
        "block":"B3",
        "room_number":"B310"
    }

def test_sign_up():
    
    response=client.post("/register/",json=user)
    assert response.status_code == 200
    print("test_resposne",response.json())
    response_user=client.post("/login",data={
        "username":"testUser",
        "password":"testUserPassword"
    })
    access_token=response_user.json().get("access_token")
    print("access_token",response_user.json())
    assert access_token
    response_get=client.get("/users/"+response.json().get("id"),headers={
        "Authorization":f'Bearer {access_token}'
    })
    assert response_get.status_code==200
    assert response_get.json().get("name")=="testUser"
    assert response_get.json().get("room_number")=="B310"
    

