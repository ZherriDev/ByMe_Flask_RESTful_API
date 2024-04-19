from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    get_remote_address,
    app=None,
    default_limits=["none per minute"],
    storage_uri="memory://"
)

def set_app(app):
  limiter.init_app(app)  

