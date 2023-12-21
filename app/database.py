from sqlalchemy import create_engine, Column, Integer, String, Table, MetaData
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings
import logging

engine = create_engine(str(settings.DATABASE_URI), pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)