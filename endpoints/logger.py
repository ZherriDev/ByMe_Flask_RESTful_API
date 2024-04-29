import logging, time
from .conn import Session, Log

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

class DBHandler(logging.Handler):
    def emit(self, record):
        with Session() as session:
            levelname = record.levelname
            datetime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            msg = record.getMessage()
            exc = getattr(record, 'exc', None)
            endpoint = record.pathname
            method = getattr(record, 'method', None)
            statuscode = getattr(record, 'statuscode', None)
            log = Log(level=levelname, date_time=datetime, msg=msg, exception=exc, path=endpoint, method=method, status_code=statuscode)
            session.add(log)
            session.commit()
            
            print(f'{levelname} [{datetime}] {msg} !{exc}! {endpoint} {method} {statuscode}')

db_handler = DBHandler()
logger.addHandler(db_handler)
