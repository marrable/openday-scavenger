from pydantic import BaseModel


class VisitorUpdate(BaseModel):
    id: int
    uid: str | None = None
    checked_in: str | None = None
    checked_out: str | None = None
    check_out: bool | None = None