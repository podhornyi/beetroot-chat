from contextlib import contextmanager
from typing import ContextManager, Optional
from flask import Flask

from sqlalchemy.orm.session import Session as ORMSession
from flask_sqlalchemy import SQLAlchemy

db: Optional[SQLAlchemy] = None


def init_db(app: Flask):
    global db
    db = SQLAlchemy(app)


@contextmanager
def session_scope() -> ContextManager[ORMSession]:
    """Provide a transactional scope around a series of operations."""
    session = db.session
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
