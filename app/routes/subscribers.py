from pathlib import Path
from uuid import uuid4

from fastapi import APIRouter, HTTPException, UploadFile, File, status

from app import database as db
from app.models import (
    SubscriberCreate,
    SubscriberReplace,
    SubscriberUpdate,
    SubscriberOut,
)


router = APIRouter(prefix="/subscribers", tags=["subscribers"])

UPLOAD_DIR = Path(__file__).resolve().parent.parent.parent / "uploads"
UPLOAD_DIR.mkdir(exist_ok=True)

ALLOWED_IMAGE_TYPES = {"image/jpeg", "image/png", "image/webp"}


@router.get("", response_model=list[SubscriberOut])
def list_subscribers():
    return db.list_all()


@router.get("/{sub_id}", response_model=SubscriberOut)
def get_subscriber(sub_id: int):
    record = db.get(sub_id)
    if record is None:
        raise HTTPException(status_code=404, detail="Subscriber not found")
    return record


@router.post("", response_model=SubscriberOut, status_code=status.HTTP_201_CREATED)
def create_subscriber(payload: SubscriberCreate):
    return db.create(payload.model_dump())


@router.put("/{sub_id}", response_model=SubscriberOut)
def replace_subscriber(sub_id: int, payload: SubscriberReplace):
    record = db.replace(sub_id, payload.model_dump())
    if record is None:
        raise HTTPException(status_code=404, detail="Subscriber not found")
    return record


@router.patch("/{sub_id}", response_model=SubscriberOut)
def update_subscriber(sub_id: int, payload: SubscriberUpdate):
    changes = payload.model_dump(exclude_unset=True)
    if not changes:
        raise HTTPException(status_code=400, detail="No fields provided to update")

    record = db.patch(sub_id, changes)
    if record is None:
        raise HTTPException(status_code=404, detail="Subscriber not found")
    return record


@router.delete("/{sub_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_subscriber(sub_id: int):
    if not db.delete(sub_id):
        raise HTTPException(status_code=404, detail="Subscriber not found")


@router.post("/{sub_id}/photo", response_model=SubscriberOut)
async def upload_photo(sub_id: int, file: UploadFile = File(...)):
    if db.get(sub_id) is None:
        raise HTTPException(status_code=404, detail="Subscriber not found")

    if file.content_type not in ALLOWED_IMAGE_TYPES:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type '{file.content_type}'. "
                   f"Allowed: {', '.join(sorted(ALLOWED_IMAGE_TYPES))}",
        )

    suffix = Path(file.filename or "").suffix or ".bin"
    saved_name = f"{sub_id}_{uuid4().hex}{suffix}"
    saved_path = UPLOAD_DIR / saved_name

    contents = await file.read()
    saved_path.write_bytes(contents)

    photo_url = f"/uploads/{saved_name}"
    return db.set_photo_url(sub_id, photo_url)
