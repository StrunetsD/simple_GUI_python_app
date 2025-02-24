from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

from settings.config import DATABASE_URL

engine = create_engine(DATABASE_URL, echo=True)

Base = declarative_base()
