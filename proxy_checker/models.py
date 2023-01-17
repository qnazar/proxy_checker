import datetime

from sqlalchemy import create_engine, Column, Integer, String, DECIMAL, Boolean, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base
from settings import *


Base = declarative_base()


def db_connect():
    return create_engine(f'postgresql+psycopg2://{PG_USER}:{PG_PSSWRD}@{PG_HOST}:{PG_PORT}/{PG_DATABASE}')


def create_table(engine):
    Base.metadata.create_all(engine)


def get_session(engine):
    session = sessionmaker(bind=engine)
    return session


class Proxy(Base):
    __tablename__ = 'Proxies'

    ip = Column(String(32), primary_key=True)
    port = Column(String(8), primary_key=True)
    country_code = Column(String(2), nullable=False)
    country = Column(String(32), nullable=False)
    secure = Column(Boolean, nullable=False)
    is_alive = Column(Boolean, default=False)
    availability = Column(DECIMAL(precision=5, scale=2, asdecimal=True), default=0.0)
    ping = Column(DECIMAL(precision=5, scale=4, asdecimal=True))
    is_clean = Column(Boolean, default=False)
    check_passed = Column(Integer, default=0)
    total_checks = Column(Integer, default=0)
    added_at = Column(DateTime, default=datetime.datetime.now())
    last_checked = Column(DateTime)
