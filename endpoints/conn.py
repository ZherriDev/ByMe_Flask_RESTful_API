from sqlalchemy import create_engine, Column, Integer, String, BigInteger, DateTime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import SQLAlchemyError
import logging, subprocess

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

log_file = "app.log"
file_handler = logging.FileHandler(log_file)    
formatter = logging.Formatter('%(levelname)s : %(message)s : %(asctime)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

file_handler.setLevel(logging.DEBUG)

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
    exception = Column(String, nullable=True)
    path = Column(String, nullable=True)
    method = Column(String, nullable=True)
    status_code = Column(Integer, nullable=True)

try:
    engine.connect()
    logger.info('Sucesssfully connection to database')
except SQLAlchemyError as e:
    logger.critical('Failed to establish database connection. Application shutting down')
    subprocess.Popen("pkill -f 'gunicorn'", shell=True)
