import io

import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_get_list_returns_seeded_data():
    r = client.get("/subscribers")
    assert r.status_code == 200
    assert isinstance(r.json(), list)
    assert len(r.json()) >= 1


def test_get_single_ok():
    r = client.get("/subscribers/1")
    assert r.status_code == 200
    assert r.json()["id"] == 1


def test_get_single_not_found():
    r = client.get("/subscribers/99999")
    assert r.status_code == 404


def test_post_creates_subscriber():
    r = client.post("/subscribers", json={
        "name": "Test User",
        "email": "test@example.com",
        "membership_type": "basic",
        "active": True,
    })
    assert r.status_code == 201
    assert r.json()["id"] > 0
    assert r.json()["photo_url"] is None


def test_post_rejects_bad_email():
    r = client.post("/subscribers", json={
        "name": "X", "email": "not-an-email", "membership_type": "basic",
    })
    assert r.status_code == 422


def test_put_replaces_record():
    created = client.post("/subscribers", json={
        "name": "Old", "email": "old@example.com",
        "membership_type": "basic", "active": True,
    }).json()
    r = client.put(f"/subscribers/{created['id']}", json={
        "name": "New", "email": "new@example.com",
        "membership_type": "premium", "active": False,
    })
    assert r.status_code == 200
    assert r.json()["name"] == "New"


def test_put_requires_all_fields():
    r = client.put("/subscribers/1", json={"name": "only name"})
    assert r.status_code == 422


def test_patch_preserves_unspecified_fields():
    created = client.post("/subscribers", json={
        "name": "Before", "email": "before@example.com",
        "membership_type": "basic", "active": True,
    }).json()
    r = client.patch(f"/subscribers/{created['id']}", json={"active": False})
    assert r.status_code == 200
    assert r.json()["active"] is False
    assert r.json()["name"] == "Before"
    assert r.json()["email"] == "before@example.com"


def test_patch_empty_body_rejected():
    r = client.patch("/subscribers/1", json={})
    assert r.status_code == 400


def test_delete_then_404():
    created = client.post("/subscribers", json={
        "name": "Goner", "email": "g@example.com",
        "membership_type": "basic", "active": True,
    }).json()
    r1 = client.delete(f"/subscribers/{created['id']}")
    assert r1.status_code == 204
    r2 = client.delete(f"/subscribers/{created['id']}")
    assert r2.status_code == 404


def test_upload_photo():
    created = client.post("/subscribers", json={
        "name": "Photo User", "email": "p@example.com",
        "membership_type": "basic", "active": True,
    }).json()
    fake_png = io.BytesIO(b"\x89PNG\r\n\x1a\n" + b"\x00" * 50)
    r = client.post(
        f"/subscribers/{created['id']}/photo",
        files={"file": ("photo.png", fake_png, "image/png")},
    )
    assert r.status_code == 200
    assert r.json()["photo_url"].startswith("/uploads/")


def test_upload_rejects_bad_content_type():
    r = client.post(
        "/subscribers/1/photo",
        files={"file": ("x.exe", io.BytesIO(b"x"), "application/octet-stream")},
    )
    assert r.status_code == 400
