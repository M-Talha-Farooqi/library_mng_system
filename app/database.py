from typing import Dict, Optional
from itertools import count


_subscribers: Dict[int, dict] = {}

_id_seq = count(start=1)


def _next_id() -> int:
    return next(_id_seq)


def list_all() -> list[dict]:
    return list(_subscribers.values())


def get(sub_id: int) -> Optional[dict]:
    return _subscribers.get(sub_id)


def create(data: dict) -> dict:
    new_id = _next_id()
    record = {"id": new_id, "photo_url": None, **data}
    _subscribers[new_id] = record
    return record


def replace(sub_id: int, data: dict) -> Optional[dict]:
    if sub_id not in _subscribers:
        return None
    photo_url = _subscribers[sub_id].get("photo_url")
    _subscribers[sub_id] = {"id": sub_id, "photo_url": photo_url, **data}
    return _subscribers[sub_id]


def patch(sub_id: int, data: dict) -> Optional[dict]:
    if sub_id not in _subscribers:
        return None
    _subscribers[sub_id].update(data)
    return _subscribers[sub_id]


def delete(sub_id: int) -> bool:
    return _subscribers.pop(sub_id, None) is not None


def set_photo_url(sub_id: int, url: str) -> Optional[dict]:
    if sub_id not in _subscribers:
        return None
    _subscribers[sub_id]["photo_url"] = url
    return _subscribers[sub_id]


def seed():
    if _subscribers:
        return
    for s in [
        {"name": "Ahmad Khan",  "email": "ahmad@example.com",  "membership_type": "premium", "active": True},
        {"name": "Jamil Ahmed",   "email": "jamil@example.com",    "membership_type": "basic",   "active": True},
        {"name": "Usama Yusuf","email": "usama@example.com", "membership_type": "student", "active": False},
    ]:
        create(s)


seed()
