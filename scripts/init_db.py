"""Create the initial cs_cloud database schema from SQLAlchemy models."""

import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# Importing the package registers every ORM model with Base.metadata.
import app.models  # noqa: F401, E402
from app.database import Base, engine  # noqa: E402


def main() -> None:
    """Create all registered ORM tables if they do not already exist."""
    Base.metadata.create_all(bind=engine)
    print("Database schema initialized successfully.")


if __name__ == "__main__":
    main()
