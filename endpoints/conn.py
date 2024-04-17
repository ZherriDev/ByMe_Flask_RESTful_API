from sqlalchemy import create_engine, Column, Integer, String, BigInteger, DateTime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import SQLAlchemyError

user_db = 'BymeDB_bricklift'
password_db = 'e40f766b1e3ab2a917d8328d912757f02b0a8d82'
host_db = '8r0.h.filess.io'
port_db = 3307
database_db = 'BymeDB_bricklift'

engine = create_engine(f'mysql+pymysql://{user_db}:{password_db}@{host_db}:{port_db}/{database_db}')
Session = sessionmaker(bind=engine)

Base = declarative_base()

class Log(Base):
    __tablename__ = "logs"

    log_id = Column(BigInteger, primary_key=True, autoincrement=True)
    level = Column(String, nullable=True)
    date_time = Column(DateTime, nullable=True)
    msg = Column(String, nullable=True)
    endpoint = Column(String, nullable=True)
    method = Column(String, nullable=True)
    status_code = Column(Integer, nullable=True)