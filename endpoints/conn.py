from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

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
    
    log_id = Column(Integer, primary_key=True)