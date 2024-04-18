from flask import jsonify, request,  Blueprint
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity
from sqlalchemy import text
from ..conn import Session
from ..logger import logger
from datetime import datetime
import subprocess

shutdown_bp = Blueprint('shutdown', __name__)

@shutdown_bp.route('/shutdown', methods=['GET'])
@jwt_required()
def shutdown():
    doctor_id = get_jwt_identity()
    claims = get_jwt()
    
    if "admin" in claims:
        subprocess.Popen("pkill -f 'gunicorn'", shell=True)
        logger.critical(f"Admin ID:{doctor_id} shut down the server.", extra={"method": "GET", "statuscode": 200})
        return jsonify({'success': True, 'msg': 'Shutting down...'}), 200
    else:
        logger.warning(f"Someone tried to shut down the server without permission.", extra={"method": "GET", "statuscode": 403})
        return jsonify({'error': 'Access Denied'}), 403
