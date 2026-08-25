"""Steam account ORM model."""

from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class SteamAccount(Base):
    __tablename__ = "steam_accounts"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    steam_id: Mapped[str] = mapped_column(String(32), unique=True, index=True, nullable=False)
    account_name: Mapped[str] = mapped_column(String(100), nullable=False)
    status: Mapped[str] = mapped_column(String(30), nullable=False, default="active", server_default="active")
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )

    user: Mapped["User"] = relationship(back_populates="steam_accounts")
    inventory_items: Mapped[list["InventoryItem"]] = relationship(
        back_populates="steam_account", cascade="all, delete-orphan"
    )
