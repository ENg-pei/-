"""User ORM model."""

from datetime import datetime

from sqlalchemy import DateTime, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )

    steam_accounts: Mapped[list["SteamAccount"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )
    alchemy_tasks: Mapped[list["AlchemyTask"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )
    operation_logs: Mapped[list["OperationLog"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )
