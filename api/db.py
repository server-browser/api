from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session

from api.config import DEBUG, SQLALCHEMY_DATABASE_URI

engine = create_engine(
    SQLALCHEMY_DATABASE_URI
)

if DEBUG:
    print(SQLALCHEMY_DATABASE_URI)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

from api.logger import get_logger

__logger = get_logger(__name__)

def get_session_local() -> Session:
    """same as SessionLocal but with right type hint

    Returns:
        Session: a DB session
    """
    return SessionLocal()

def get_db() -> Session:
    db = get_session_local()
    try:
        yield db
    except Exception as ex:
        __logger.exception(ex)
        db.rollback()
        raise ex
    finally:
        db.close()