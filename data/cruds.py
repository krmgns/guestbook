from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from .models import User, Entry
from .errors import ConflictError
from .schemas import (
    UserIn, UserOut, UserOutList,
    EntryIn, EntryOut, EntryOutList
)
from datetime import datetime
import math

class DAO():
    """
    Base Data Access Object class for UserDAO & EntryDAO classes.
    """
    def __init__(self, db: Session):
        """
        Store "db" var for subclasses.
        """
        self.db = db

    @staticmethod
    def paginate(page: int, limit: int, count: int) -> tuple:
        """
        Pagination helper method.
        For the sake of KISS & safety.
        """
        # Simple safety measures.
        page, limit = map(abs, [page, limit])
        page, limit = max(page, 1), max(limit, 1)

        offset = (page * limit) - limit
        total_pages = int(math.ceil(count / limit))

        return page, limit, offset, total_pages

class UserDAO(DAO):
    """
    Data Access Object for users, for saving and listing
    user related records.
    """
    def all(self) -> UserOutList:
        """
        Fetch all users and prepare as its list.
        """
        rows = self.db.query(
                # Select needed fields only (optimise data transfer load).
                User.name, User.message_count,
                Entry.subject, Entry.message
            ) \
            .join(
                Entry, Entry.user_id == User.id,
                # If isouter not true, users with no entries won't come
                # as it then runs JOIN instead LEFT JOIN.
                isouter=True
            ) \
            .order_by(
                # Required to suppress error: DISTINCT ON expressions
                # must match initial ORDER BY expressions.
                User.name,
                # To bring last records to top.
                Entry.id.desc()
            ) \
            .distinct(
                # Thanks to distinct(), no subquery used anyway.
                User.name
            ) \
            .all()

        users = []
        for row in rows:
            last_entry = None
            if row.subject is not None:
                last_entry = "%s | %s" \
                    % (row.subject, row.message)

            users.append(UserOut(
                username=row.name,
                last_entry=last_entry,
                total_count_of_messages=row.message_count
            ))

        return UserOutList(users=users)

    def add(self, user: UserIn) -> User:
        """
        Add a new user, raise a `ConflictError` if user name exists.
        @internal
        """
        found = self.db.query(User.id) \
            .filter(User.name == user.name) \
            .first()

        if found is not None:
            raise ConflictError()

        # Modify timestamp.
        data = user.dict()
        data["created_at"] = datetime.now()

        user = User(**data)
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)

        return user

class EntryDAO(DAO):
    """
    Data Access Object for entries, for saving and listing
    entry related records.
    """
    def all(self, page: int = 1, limit: int = 3) -> EntryOutList:
        """
        Fetch all entries and prepare as its list.
        """
        count = self.db.query(func.count(Entry.id)).scalar()

        # Do pagination with taken row count.
        page, limit, offset, total = DAO.paginate(page, limit, count)

        rows = self.db.query(
                # Select needed fields only (optimise data transfer load).
                Entry.subject, Entry.message,
                User.name
            ) \
            .join(User, User.id == Entry.user_id) \
            .order_by(Entry.created_at.desc()) \
            .offset(offset).limit(limit) \
            .all()

        entries = []
        for row in rows:
            entries.append(EntryOut(
                user=row.name,
                subject=row.subject,
                message=row.message
            ))

        entries = EntryOutList(
            count=count,
            page_size=limit,
            total_pages=total,
            current_page_number=page,
            entries=entries
        )

        # Update prev/next links.
        entries.update_links()

        return entries

    def add(self, entry: EntryIn) -> Entry:
        """
        Add a new entry for a user, create if user is absent.
        """
        user = self.db.query(User) \
            .filter(User.name == entry.name) \
            .first()

        # No ConflictError check, since it's being done here.
        if user is None:
            user = UserDAO(self.db).add(UserIn(name=entry.name))

        # Update user's message count, so let the reads be free from count()
        # calls in persistence layer.
        # @note Here I'd be counting all related entry rows and using it
        # instead using "1".
        user.message_count += 1

        # Modify timestamp, assign FKID and drop undefined field.
        data = entry.dict()
        data["created_at"] = datetime.now()
        data["user_id"] = user.id
        del data["name"]

        entry = Entry(**data)
        self.db.add(entry)
        self.db.commit()
        self.db.refresh(entry)

        return entry
