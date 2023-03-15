from app.cruds import bid as cruds
from app.cruds import slot as slotcruds
from conftest import test_db
from app.main import app
from app.models.models import User, Task, Slot, Bid
from sqlalchemy.future import select
import datetime
from sqlalchemy.orm import Session
import random
from app.cruds import response
user_test_data = [
    {
        "name": "user_1",
        "password": "bid_1_password",
        "block": "B3",
        "room_number": "B310",
    },
    {
        "name": "user_2",
        "password": "bid_1_password",
        "block": "B3",
        "room_number": "B310",
    },
    {
        "name": "user_3",
        "password": "bid_1_password",
        "block": "B3",
        "room_number": "B310",
    },]

task_test_data ={
        "name": "task_1",
        "detail": "bid_1_password",
        "max_woker_num": 3,
        "min_woker_num": 3,
        "exp_woker_num": 0,
    }
slot={
    "name": "slot_1",
        "start_time": {
            "year": 2022,
            "month": 12,
            "day": 30,
            "hour": 22,
            "minute": 0,
        },
        "end_time": {
            "year": 2022,
            "month": 12,
            "day": 31,
            "hour": 8,
            "minute": 0,
        },
}
bid_test_data={
    "name": "bid_1",
    "open_time": {
        "year": 2022,
        "month": 12,
        "day": 22,
        "hour": 22,
        "minute": 0,
    },
    "close_time": {
        "year": 2022,
        "month": 12,
        "day": 29,
        "hour": 8,
        "minute": 0,
    },
    "start_point": 10,
    "buyout_point": 3,
}

def test_cruds_bid_close(test_db:Session):
    db_users:list[User]=[]
    for user in user_test_data:
        db_users.append(User(
            name=user["name"],
            password=user["password"],
            block=user["block"],
            room_number=user["room_number"],
        ))
    test_db.add_all(db_users)
    test_db.commit()
    creater_id = db_users[0].id
    db_task = Task(
        name=task_test_data["name"],
        detail=task_test_data["detail"],
        max_woker_num=task_test_data["max_woker_num"],
        min_woker_num=task_test_data["min_woker_num"],
        exp_woker_num=task_test_data["exp_woker_num"],
        creater_id=creater_id
    )
    test_db.add(db_task)
    test_db.commit()
    db_slot = Slot(
            name=slot["name"],
            start_time=datetime.datetime(
                slot["start_time"]["year"],
                slot["start_time"]["month"],
                slot["start_time"]["day"],
                slot["start_time"]["hour"],
                slot["start_time"]["minute"],
            ),
            end_time=datetime.datetime(
                slot["end_time"]["year"],
                slot["end_time"]["month"],
                slot["end_time"]["day"],
                slot["end_time"]["hour"],
                slot["end_time"]["minute"],
            ),
            task_id=db_task.id,
            creater_id=creater_id,
        )
    print(db_slot.template,'before')
    test_db.add(db_slot)
    test_db.commit()
    assert_slot=test_db.get(Slot,db_slot.id)
    print(assert_slot.template,'after')
    db_bid=  Bid(
            name="test_close_bid",
            open_time=datetime.datetime(
                bid_test_data["open_time"]["year"],
                bid_test_data["open_time"]["month"],
                bid_test_data["open_time"]["day"],
                bid_test_data["open_time"]["hour"],
                bid_test_data["open_time"]["minute"],
            ),
            close_time=datetime.datetime(
                bid_test_data["close_time"]["year"],
                bid_test_data["close_time"]["month"],
                bid_test_data["close_time"]["day"],
                bid_test_data["close_time"]["hour"],
                bid_test_data["close_time"]["minute"],
            ),
            slot_id=db_slot.id,
            start_point=10,
            buyout_point=3,
        )
    test_db.add(db_bid)
    test_db.commit()
    test_db.commit()
    _=cruds.tender(db_bid.id,tender_point=9,user=db_users[0],db=test_db)
    _=cruds.tender(db_bid.id,tender_point=8,user=db_users[1],db=test_db)
    _=cruds.tender(db_bid.id,tender_point=7,user=db_users[2],db=test_db)
    closed_slot=cruds.close(db_bid.id,test_db)
    print(closed_slot["assignees"])
    assert closed_slot["assignees"]==response.users_response(db_users)
    