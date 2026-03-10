import uuid
from .base import Base
from sqlalchemy import String, func, text
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID


class User(Base):
    __tablename__ = "users"

    uuid: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=func.uuidv7() # https://www.postgresql.org/docs/current/functions-uuid.html#FUNCTIONS-UUID
    )

    username: Mapped[str] = mapped_column(
        String(30),
        unique=True,
    )
    
    passhash: Mapped[str] = mapped_column(String(255)) # Vai caber o hash da maioria dos algorítmos
    