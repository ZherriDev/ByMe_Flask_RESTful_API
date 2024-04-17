from flask import jsonify, request, Blueprint
from ..conn import Session

shutdown_bp = Blueprint('shutdown', __name__)

@shutdown_bp.route('/shutdown', methods=['GET'])
def shutdown():
    