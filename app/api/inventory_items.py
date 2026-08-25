"""Inventory item CRUD endpoints."""

from collections.abc import Sequence

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import InventoryItem, SteamAccount
from app.schemas.inventory_item import InventoryItemCreate, InventoryItemRead


router = APIRouter(prefix="/inventory_items", tags=["inventory_items"])


@router.post("", response_model=InventoryItemRead, status_code=status.HTTP_201_CREATED)
def create_inventory_item(payload: InventoryItemCreate, db: Session = Depends(get_db)) -> InventoryItem:
    """Create an inventory item for an existing Steam account."""
    if db.get(SteamAccount, payload.steam_account_id) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Steam account not found")

    inventory_item = InventoryItem(**payload.model_dump())
    db.add(inventory_item)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Asset ID already exists for this Steam account",
        )

    db.refresh(inventory_item)
    return inventory_item


@router.get("", response_model=list[InventoryItemRead])
def list_inventory_items(db: Session = Depends(get_db)) -> Sequence[InventoryItem]:
    """Return all inventory items ordered by ID."""
    return db.scalars(select(InventoryItem).order_by(InventoryItem.id)).all()


@router.get("/{inventory_item_id}", response_model=InventoryItemRead)
def get_inventory_item(inventory_item_id: int, db: Session = Depends(get_db)) -> InventoryItem:
    """Return one inventory item by ID."""
    inventory_item = db.get(InventoryItem, inventory_item_id)
    if inventory_item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Inventory item not found")
    return inventory_item
