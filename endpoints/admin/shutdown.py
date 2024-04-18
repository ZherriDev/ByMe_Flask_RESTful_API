from flask import jsonify, request,  Blueprint
from ..conn import Session
import subprocess

shutdown_bp = Blueprint('shutdown', __name__)

@shutdown_bp.route('/shutdown', methods=['GET'])
def shutdown():
    if request.remote_addr == '127.0.0.1':
        subprocess.Popen("pkill -f 'gunicorn'", shell=True)
        return jsonify({'success': True, 'msg': 'Shutting down...'}), 200
    else:
        return jsonify({'error': 'Access Denied'}), 403