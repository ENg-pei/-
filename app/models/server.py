"""Server ORM model."""

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Server(Base):
    __tablename__ = "servers"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    ip: Mapped[str] = mapped_column(String(45), unique=True, nullable=False)
    status: Mapped[str] = mapped_column(String(30), nullable=False, default="active", server_default="active")
