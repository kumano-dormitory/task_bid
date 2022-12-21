from fastapi.testclient import TestClient
from app.main import app

client=TestClient(app)

def test_add_task():
    task={
        "name":"testtask",
        "detail":"This is the task json for testing (これはテスト用のTaskオブジェクトです)",
        "authority":["1","2","3",],
        "tag":["1","2","3"]
    }
    response=client.post("/tasks/",json=task)
    assert response.status_code == 200

    
    

