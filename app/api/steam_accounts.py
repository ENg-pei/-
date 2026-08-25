"""Steam account CRUD endpoints."""

from collections.abc import Sequence

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import SteamAccount, User
from app.schemas.steam_account import SteamAccountCreate, SteamAccountRead


router = APIRouter(prefix="/steam_accounts", tags=["steam_accounts"])


@router.post("", response_model=SteamAccountRead, status_code=status.HTTP_201_CREATED)
def create_steam_account(payload: SteamAccountCreate, db: Session = Depends(get_db)) -> SteamAccount:
    """Create a Steam account for an existing user."""
    if db.get(User, payload.user_id) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    steam_account = SteamAccount(**payload.model_dump())
    db.add(steam_account)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Steam ID already exists")

    db.refresh(steam_account)
    return steam_account


@router.get("", response_model=list[SteamAccountRead])
def list_steam_accounts(db: Session = Depends(get_db)) -> Sequence[SteamAccount]:
    """Return all Steam accounts ordered by ID."""
    return db.scalars(select(SteamAccount).order_by(SteamAccount.id)).all()


@router.get("/{steam_account_id}", response_model=SteamAccountRead)
def get_steam_account(steam_account_id: int, db: Session = Depends(get_db)) -> SteamAccount:
    """Return one Steam account by ID."""
    steam_account = db.get(SteamAccount, steam_account_id)
    if steam_account is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Steam account not found")
    return steam_account
