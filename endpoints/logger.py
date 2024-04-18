import logging
from .conn import Session, Log

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

class DBHandler(logging.Handler):
    def emit(self, record):
        with Session() as session:
            levelname = record.levelname
            datetime = record.asctime
            msg = record.getMessage()
            endpoint = record.pathname
            method = getattr(record, 'method', None)
            statuscode = getattr(record, 'statuscode', None)
            log = Log(level=levelname, date_time=datetime, msg=msg, path=endpoint, method=method, status_code=statuscode)
            session.add(log)
            session.commit()
            
            print(f'{levelname} [{datetime}] {msg} {endpoint} {method} {statuscode}')

db_handler = DBHandler()
logger.addHandler(db_handler)
