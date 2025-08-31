from typing import Generator
from app.core.database import get_database


def get_db() -> Generator:
    # yield a pymongo database instance
    db = get_database()
    try:
        yield db
    finally:
        # pymongo doesn't require closing the database handle here
        pass
