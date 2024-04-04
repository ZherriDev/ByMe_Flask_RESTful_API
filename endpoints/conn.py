from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

user_db = 'sql11696357'
password_db = 'Qp4hRnMDZY'
host_db = 'sql11.freesqldatabase.com'
port_db = 3306
database_db = 'sql11696357'

engine = create_engine(f'mysql+pymysql://{user_db}:{password_db}@{host_db}:{port_db}/{database_db}')
Session = sessionmaker(bind=engine)