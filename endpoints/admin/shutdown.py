from flask import jsonify, request, Blueprint
from ..conn import Session

shutdown_bp = Blueprint('shutdown', __name__)

@shutdown_bp.route('/shutdown', methods=['GET'])
def shutdown():
    if request.remote_addr == '127.0.0.1':
        shutdown_func = request.environ.get('werkzeug.server.shutdown')
        if shutdown_func is None:
            return jsonify({'error': 'no shutdown function'}), 500
        
        shutdown_func()
        return jsonify({'success': True, 'msg': 'Shutting down...'}), 200
    else:
        return jsonify({'error': 'Access Denied'}), 403