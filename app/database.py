from sqlalchemy import create_engine, Column, Integer, String, Table, MetaData
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import sessionmaker, declarative_base

from app.core.config import settings

engine = create_engine(str(settings.DATABASE_URI), pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
metadata = MetaData()
users = Table(
    'users',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('username', String),
    Column('password', String),
    Column('email', String),
    Column('full_name', String),
)
metadata.create_all(engine)

Base = declarative_base()
class Base:
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()