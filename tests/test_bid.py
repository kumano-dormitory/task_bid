from app.cruds import bid as cruds
from app.cruds import slot as slotcruds
from conftest import test_db
from app.main import app
from app.models.models import User, Task, Slot, Bid
from sqlalchemy.future import select
import datetime
from sqlalchemy.orm import Session
import random

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
    },
    {
        "name": "user_4",
        "password": "bid_1_password",
        "block": "B3",
        "room_number": "B310",
    },
    {
        "name": "user_5",
        "password": "bid_1_password",
        "block": "B3",
        "room_number": "B310",
    },
    {
        "name": "user_6",
        "password": "bid_1_password",
        "block": "B3",
        "room_number": "B310",
    },
    {
        "name": "user_7",
        "password": "bid_1_password",
        "block": "B3",
        "room_number": "B310",
    },
    {
        "name": "user_8",
        "password": "bid_1_password",
        "block": "B3",
        "room_number": "B310",
    },
    {
        "name": "user_9",
        "password": "bid_1_password",
        "block": "B3",
        "room_number": "B310",
    },
    {
        "name": "user_10",
        "password": "bid_1_password",
        "block": "B3",
        "room_number": "B310",
    },
    {
        "name": "user_11",
        "password": "bid_1_password",
        "block": "B3",
        "room_number": "B310",
    },
    {
        "name": "user_12",
        "password": "bid_1_password",
        "block": "B3",
        "room_number": "B310",
    },
    {
        "name": "user_13",
        "password": "bid_1_password",
        "block": "B3",
        "room_number": "B310",
    },
    {
        "name": "user_14",
        "password": "bid_1_password",
        "block": "B3",
        "room_number": "B310",
    },
    {
        "name": "user_15",
        "password": "bid_1_password",
        "block": "B3",
        "room_number": "B310",
    },
    {
        "name": "user_16",
        "password": "bid_1_password",
        "block": "B3",
        "room_number": "B310",
    },
    {
        "name": "user_17",
        "password": "bid_1_password",
        "block": "B3",
        "room_number": "B310",
    },
    {
        "name": "user_18",
        "password": "bid_1_password",
        "block": "B3",
        "room_number": "B310",
    },
    {
        "name": "user_19",
        "password": "bid_1_password",
        "block": "B3",
        "room_number": "B310",
    },
    {
        "name": "user_20",
        "password": "bid_1_password",
        "block": "B3",
        "room_number": "B310",
    },
]
task_test_data = [
    {
        "name": "task_1",
        "detail": "bid_1_password",
        "max_woker_num": 3,
        "min_woker_num": 3,
        "exp_woker_num": 3,
    },
    {
        "name": "task_2",
        "detail": "bid_1_password",
        "max_woker_num": 3,
        "min_woker_num": 3,
        "exp_woker_num": 2,
    },
    {
        "name": "task_3",
        "detail": "bid_1_password",
        "max_woker_num": 3,
        "min_woker_num": 1,
        "exp_woker_num": 1,
    },
    {
        "name": "task_4",
        "detail": "bid_1_password",
        "max_woker_num": 2,
        "min_woker_num": 1,
        "exp_woker_num": 1,
    },
    {
        "name": "task_5",
        "detail": "bid_1_password",
        "max_woker_num": 9,
        "min_woker_num": 8,
        "exp_woker_num": 4,
    },
]
slot_test_data = [
    {
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
    },
    {
        "name": "slot_2",
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
    },
    {
        "name": "slot_3",
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
    },
    {
        "name": "slot_4",
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
    },
    {
        "name": "slot_5",
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
    },
]
bid_test_data = [
    {
        "name": "bid_1",
        "open_time": {
            "year": 2022,
            "month": 12,
            "day": 30,
            "hour": 22,
            "minute": 0,
        },
        "close_time": {
            "year": 2022,
            "month": 12,
            "day": 31,
            "hour": 8,
            "minute": 0,
        },
        "start_point": 10,
        "buyout_point": 3,
    },
    {
        "name": "bid_1",
        "open_time": {
            "year": 2022,
            "month": 12,
            "day": 30,
            "hour": 22,
            "minute": 0,
        },
        "close_time": {
            "year": 2022,
            "month": 12,
            "day": 31,
            "hour": 8,
            "minute": 0,
        },
        "start_point": 10,
        "buyout_point": 3,
    },
    {
        "name": "bid_1",
        "open_time": {
            "year": 2022,
            "month": 12,
            "day": 30,
            "hour": 22,
            "minute": 0,
        },
        "close_time": {
            "year": 2022,
            "month": 12,
            "day": 31,
            "hour": 8,
            "minute": 0,
        },
        "start_point": 10,
        "buyout_point": 3,
    },
]


def test_cruds_bid_close(test_db: Session):
    for user in user_test_data:
        db_user = User(
            name=user["name"],
            password=user["password"],
            block=user["block"],
            room_number=user["room_number"],
        )
        test_db.add(db_user)
    test_db.flush()
    test_db.commit()
    creater = test_db.scalars(
        select(User).filter(User.name == "user_1")
    ).first()
    for task in task_test_data:
        db_task = Task(
            name=task["name"],
            detail=task["detail"],
            max_woker_num=task["max_woker_num"],
            min_woker_num=task["min_woker_num"],
            exp_woker_num=task["exp_woker_num"],
        )
        test_db.add(db_task)
    test_db.flush()
    test_db.commit()
    tasks = test_db.scalars(select(Task)).unique().all()
    db_slot_list = []
    for index, slot in enumerate(slot_test_data):
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
            task_id=tasks[index].id,
            creater_id=creater.id,
        )
        assert db_slot.name == slot["name"]
        db_slot_list.append(db_slot)
    assert db_slot_list != []
    test_db.add_all(db_slot_list)
    test_db.flush()
    test_db.commit()
    for index in range(10):
        user = test_db.scalars(
            select(User)
            .filter(User.name == user_test_data[index]["name"])
            .limit(1)
        ).first()
        for task in task_test_data:
            task = test_db.scalars(
                select(Task).filter(Task.name == task["name"]).limit(1)
            ).first()
            user.exp_task.append(task)
    test_db.flush()
    test_db.commit()
    slots = test_db.execute(select(Slot)).scalars().all()
    assert slots != None
    assert len(slots) == 5
    db_bid_list = []
    for index, slot in enumerate(slots):
        bid = Bid(
            name="bid_" + str(index),
            open_time=datetime.datetime(
                slot_test_data[index]["start_time"]["year"],
                slot_test_data[index]["start_time"]["month"],
                slot_test_data[index]["start_time"]["day"],
                slot_test_data[index]["start_time"]["hour"],
                slot_test_data[index]["start_time"]["minute"],
            ),
            close_time=datetime.datetime(
                slot_test_data[index]["end_time"]["year"],
                slot_test_data[index]["end_time"]["month"],
                slot_test_data[index]["end_time"]["day"],
                slot_test_data[index]["end_time"]["hour"],
                slot_test_data[index]["end_time"]["minute"],
            ),
            slot_id=slot.id,
            start_point=10,
            buyout_point=3,
        )
        db_bid_list.append(bid)
    test_db.add_all(db_bid_list)
    test_db.flush()
    test_db.commit()
    iter = 10
    bids = test_db.execute(select(Bid)).scalars().all()
    assert len(bids) == 5
    for bid in bids:
        exp_num = random.randint(0, 9)
        not_exp_num = random.randint(0, 9)
        for exp_index in range(exp_num):
            user = test_db.scalars(
                select(User)
                .filter(User.name == user_test_data[exp_index]["name"])
                .limit(1)
            ).first()
            cruds.tender(bid.id, random.randint(3, 10), user, test_db)
        for exp_index in range(not_exp_num):
            user = test_db.scalars(
                select(User)
                .filter(User.name == user_test_data[10 + exp_index]["name"])
                .limit(1)
            ).first()
            cruds.tender(bid.id, random.randint(3, 10), user, test_db)
        response = cruds.close(bid.id, test_db)
        assert response != None
        print("slot", response)
        for assignee in response["assignees"]:
            print("assignee", assignee)
        current_user = test_db.get(User, response["assignees"][0]["id"])
        slot = slotcruds.cancel(response["id"], current_user, 3, test_db)
        assert slot != None

    assert test_db != None
