from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from data.connection import Base, engine, connection
from data.schemas import UserOutList, EntryOutList, EntryIn
from data.cruds import UserDAO, EntryDAO
from __util import JSONResponse

# Ensure tables exist.
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Guest Book")

@app.get("/users", response_model=UserOutList)
def get_users(
    db: Session = Depends(connection)
) -> JSONResponse:
    """
    Get users list.
    @note As it's noted in docs, no pagination available here.
    """
    users = UserDAO(db).all()
    return JSONResponse(200, users)

@app.get("/entries", response_model=EntryOutList)
def get_entries(
    page: int = 1, limit: int = 3,
    db: Session = Depends(connection)
) -> JSONResponse:
    """
    Get entries list.
    @note As it's noted in docs, pagination is available here,
    with page/limit query params.
    """
    entries = EntryDAO(db).all(page, limit)
    return JSONResponse(200, entries)

@app.post("/entries")
def add_entry(
    entry: EntryIn,
    db: Session = Depends(connection)
) -> JSONResponse:
    """
    Add new entry.
    """
    try:
        entry = EntryDAO(db).add(entry)
        return JSONResponse(200, entry)
    except Exception as e:
        return JSONResponse(500, {"error": "Internal error", "detail": str(e)})
