from flask import jsonify, request,  Blueprint
from flask_jwt_extended import jwt_required, verify_jwt_in_request, get_jwt_identity
from sqlalchemy import text
from ..conn import Session
from ..logger import logger
from datetime import datetime
import subprocess

shutdown_bp = Blueprint('shutdown', __name__)

@shutdown_bp.route('/shutdown', methods=['GET'])
@jwt_required()
def shutdown():
    jwt_token = verify_jwt_in_request()
    doctor_id = get_jwt_identity()
    
    session = Session()
    
    try:
        result = session.execute(
            text("SELECT name, admin FROM doctors WHERE doctor_id : :doctor_id"),
            {"doctor_id": doctor_id}
        ).fetchone()
        
        name = result[0]
        isAdmin = result[1]
        
        if isAdmin == 1:
            subprocess.Popen("pkill -f 'gunicorn'", shell=True)
            logger.critical(f"Admin {name} turned off the server.", extra={"method": "GET", "statuscode": 200, "datetime": datetime.now()})
            return jsonify({'success': True, 'msg': 'Shutting down...'}), 200
        else:
            logger.warning(f"", extra={"method": "GET", "statuscode": 403, "datetime": datetime.now()})
            return jsonify({'error': 'Access Denied'}), 403
    except Exception as e:
        session.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        session.close()