from pydantic import BaseModel
from datetime import datetime
from typing import List

class UserIn(BaseModel):
    name: str
    # For updates only.
    created_at: datetime = None

class UserOut(BaseModel):
    username: str
    last_entry: str = None
    total_count_of_messages: int = 0

class UserOutList(BaseModel):
    users: List[UserOut] = None

class EntryIn(BaseModel):
    name: str
    subject: str
    message: str
    # For updates only.
    created_at: datetime = None

class EntryOut(BaseModel):
    user: str
    subject: str
    message: str

class EntryOutList(BaseModel):
    count: int = None
    page_size: int = None
    total_pages: int = None
    current_page_number: int = None
    links: dict = {"next": None, "previous": None}
    entries: List[EntryOut] = None

    def update_links(self):
        """
        Update this list's links.
        """
        if self.total_pages > 0:
            if (self.current_page_number + 1) <= self.total_pages:
                next_link = "/entries?page=" + str(self.current_page_number + 1)

                # Add limit, if not default (as given in docs).
                if self.page_size != 3:
                    next_link += "&limit=" + str(self.page_size)

                self.links["next"] = next_link

            if (self.current_page_number - 1) >= 1:
                prev_link = "/entries?page=" + str(self.current_page_number - 1)

                # Add limit, if not default (as given in docs).
                if self.page_size != 3:
                    prev_link += "&limit=" + str(self.page_size)

                self.links["previous"] = prev_link

