from contextlib import contextmanager

from sqlalchemy.orm import sessionmaker

from base import engine

Session = sessionmaker(bind=engine, expire_on_commit=False)


@contextmanager
def get_session():
    session = Session()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback() #отмена всех изменений
        raise
    finally:
        session.close()
