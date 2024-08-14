# Before Beginning
Please be sure that you've created `guestbook` database in PostgreSQL and also updated credentials in `.env` file. After installing and running the application, you can see API documents on [http://localhost:8000/docs](http://localhost:8000/docs) and [http://localhost:8000/redoc](http://localhost:8000/redoc) links.

Note: I used an old Python version (3.6.9) due to my computer conditions.

## Environment & Versions

- Ubuntu: 18.04.6 LTS (bionic, 64-bit)
- Python: 3.6.9
- FastAPI: 0.83.0
- SQLAlchemy: 1.4.52
- Psycopg2: 2.9.8 (libpq adapter)
- Uvicorn: 0.16.0 (with CPython 3.6.9)
- PostgreSQL: 13.9 (Ubuntu 13.9-1.pgdg18.04+1)

## Creating Application Directory
    mdkir -p /path/to/dir ; cd /path/to/dir
    unzip guestbook.zip ; cd guestbook

## Installing Dependencies
    python -m pip install fastapi sqlalchemy psycopg2 uvicorn[standard]

## Running Application
    python -m uvicorn main:app --reload --port=8000

## Running Tests
    python -m unittest test.py

## Endpoints

### `GET /users`
List all users.

*Note: As it's noted in docs, `/users` endpoint cannot be paginated.* <br>
*Note: As it's noted in docs, `last_entry` field combines user's last subject and message.*

### Request
    /users

### Response
```json
{
  "users": [
    {
      "username": "Kerem",
      "last_entry": "Kerem's subject | Kerem's message",
      "total_count_of_messages": 1
    },
    ...
  ]
}
```

### `GET /entries`
List all entries.

#### Query Parameters
| Name  | Type | Default |
| ----- | ---- | ------- |
| page  | int  | 1       |
| limit | int  | 3       |

### Request
    /entries?page=1
    /entries?page=1&limit=5

### Response
```json
{
  "count": 10,
  "page_size": 3,
  "total_pages": 2,
  "current_page_number": 1,
  "links": {
    "next": "/entries?page=2",
    "previous": null
  },
  "entries": [
    {
      "user": "Kerem",
      "subject": "Kerem's subject",
      "message": "Kerem's message"
    },
    ...
  ]
}
```

### `POST /entries`
Add a new entry

### Body Parameters
| Name    | Type   | Default |
| -       | -      | -       |
| name    | String | -       |
| subject | String | -       |
| message | String | -       |

### Request
```json
{
  "name": "Test user",
  "subject": "Test subject",
  "message": "Test message"
}
```

### Response
```json
{
  "id": 123,
  "created_at": "2024-08-14T17:10:34.289374",
  "subject": "Test subject",
  "message": "Test message",
  "user_id": 123
}
```

## Notes
There's no `total_count_of_messages` field in given JSON example for `/users` endpoint, and I improvised and implemented it anyway, as it's mentioned in docs like **total count of messages** in **Get users’ data** part. Please see `data.models.User` and `data.cruds.EntryDAO.add()` code for details.
