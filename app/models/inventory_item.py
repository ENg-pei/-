"""Steam inventory item ORM model."""

from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class InventoryItem(Base):
    __tablename__ = "inventory_items"
    __table_args__ = (
        UniqueConstraint("steam_account_id", "asset_id", name="uq_inventory_items_account_asset"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    steam_account_id: Mapped[int] = mapped_column(
        ForeignKey("steam_accounts.id", ondelete="CASCADE"), nullable=False
    )
    asset_id: Mapped[str] = mapped_column(String(32), nullable=False)
    item_name: Mapped[str] = mapped_column(String(255), nullable=False)
    item_type: Mapped[str] = mapped_column(String(100), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False, default=1, server_default="1")
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )

    steam_account: Mapped["SteamAccount"] = relationship(back_populates="inventory_items")
