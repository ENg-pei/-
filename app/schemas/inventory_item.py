"""Pydantic schemas for inventory item API payloads."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class InventoryItemCreate(BaseModel):
    steam_account_id: int = Field(gt=0)
    asset_id: str = Field(min_length=1, max_length=32)
    item_name: str = Field(min_length=1, max_length=255)
    item_type: str = Field(min_length=1, max_length=100)
    quantity: int = Field(ge=1)


class InventoryItemRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    steam_account_id: int
    asset_id: str
    item_name: str
    item_type: str
    quantity: int
    created_at: datetime
