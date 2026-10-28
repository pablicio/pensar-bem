from collections.abc import Generator

from sqlalchemy.orm import Session


def get_session() -> Generator[Session, None, None]:
    with SessionLocal() as session:
        yield session
