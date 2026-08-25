"""Pydantic schemas for Steam account API payloads."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class SteamAccountCreate(BaseModel):
    user_id: int = Field(gt=0)
    steam_id: str = Field(min_length=1, max_length=32)
    account_name: str = Field(min_length=1, max_length=100)


class SteamAccountRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    steam_id: str
    account_name: str
    status: str
    created_at: datetime
