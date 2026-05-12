# Library Subscription API

A small FastAPI app for teaching REST. Every HTTP method from the lecture
slides (GET, POST, PUT, PATCH, DELETE) is demonstrated by one endpoint, plus
a file-upload endpoint for profile photos.

## Project structure

```
library_api/
├── app/
│   ├── __init__.py
│   ├── main.py            # FastAPI app entry point, CORS, static mounts
│   ├── models.py          # Pydantic schemas (Create / Replace / Update / Out)
│   ├── database.py        # Simple in-memory "DB" 
│   ├── routes/
│   │   ├── __init__.py
│   │   └── subscribers.py # All subscriber endpoints (one per HTTP method)
│   └── static/
│       └── index.html     # Single-page demo frontend
├── uploads/               # Uploaded profile photos land here
├── requirements.txt
└── README.md
```

Why this layout? Each file has one job:

- **routes/** holds HTTP-facing code only (URLs, status codes).
- **models.py** holds the data contract — request bodies and responses.
- **database.py** holds storage logic. Replacing it with SQLAlchemy later
  would not touch the route handlers.

This separation is what the slides call a *layered system* (Slide 12).

## Setup

```bash
# 1. Create a virtual environment
python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the server (reload on file changes)
uvicorn app.main:app --reload
```

Open:

- <http://127.0.0.1:8000/> — the demo web form
- <http://127.0.0.1:8000/docs> — auto-generated Swagger UI (try every endpoint here)

## HTTP methods → endpoints

| Method | Endpoint                       | What it does               | Slide |
|--------|--------------------------------|----------------------------|-------|
| GET    | `/subscribers`                 | List all subscribers       | 18    |
| GET    | `/subscribers/{id}`            | Get one subscriber         | 18    |
| POST   | `/subscribers`                 | Create a new subscriber    | 20    |
| PUT    | `/subscribers/{id}`            | Replace the whole record   | 21    |
| PATCH  | `/subscribers/{id}`            | Update some fields only    | 23    |
| DELETE | `/subscribers/{id}`            | Delete a subscriber        | 22    |
| POST   | `/subscribers/{id}/photo`      | Upload a profile photo     | 20    |

### Status codes used (Slide 24)

| Code | When                                         |
|------|----------------------------------------------|
| 200  | Successful GET / PUT / PATCH (returns body)  |
| 201  | Resource created (POST)                      |
| 204  | Successful DELETE (no body)                  |
| 400  | Bad request (e.g. empty PATCH, bad filetype) |
| 404  | Resource does not exist                      |
| 422  | Request body failed validation               |

## Try it from the command line

```bash
# GET (list)
curl http://127.0.0.1:8000/subscribers

# POST (create)
curl -X POST http://127.0.0.1:8000/subscribers \
  -H "Content-Type: application/json" \
  -d '{"name":"Sara","email":"sara@example.com","membership_type":"premium","active":true}'

# PATCH (partial update — only change one field)
curl -X PATCH http://127.0.0.1:8000/subscribers/1 \
  -H "Content-Type: application/json" \
  -d '{"active": false}'

# PUT (full replacement — must send every field)
curl -X PUT http://127.0.0.1:8000/subscribers/1 \
  -H "Content-Type: application/json" \
  -d '{"name":"Alice K.","email":"alice@example.com","membership_type":"premium","active":true}'

# DELETE
curl -X DELETE http://127.0.0.1:8000/subscribers/2

# POST (file upload)
curl -X POST http://127.0.0.1:8000/subscribers/1/photo \
  -F "file=@/path/to/photo.jpg"
```

## Teaching notes

- **PUT vs PATCH** is the classic confusion point. Demo it live: PATCH the
  `active` flag (one field in the body) and show the rest stays untouched;
  then PUT and notice the body must contain every field or validation fails.
- The **request log** at the bottom of the demo page shows the method, URL,
  status code, and response body for every action — useful for showing
  students exactly what's going over the wire.
- The in-memory database resets every time the server restarts. That's
  intentional for teaching; a one-line swap to SQLite would persist data.
