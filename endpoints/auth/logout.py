from flask import jsonify, request, Blueprint, render_template
from flask_jwt_extended import jwt_required, verify_jwt_in_request, get_jwt_identity
from flask_mailman import EmailMultiAlternatives
from marshmallow import Schema, fields
from sqlalchemy import text
from ..conn import Session
from ..logger import logger

logout_bp = Blueprint('logout_bp', __name__)

@logout_bp.route('/logout', methods=['DELETE'])
@jwt_required()
def logout():
    
    jwt_data = verify_jwt_in_request()
    doctor_id = get_jwt_identity()
    
    jti = jwt_data[1]['jti']

    try:
        session = Session()

        session.execute(
            text("UPDATE sessions SET in_blacklist = 1 WHERE jti = :jti"),
            {
                'jti': jti,
            },
        )
        session.commit()
        
        logger.info(f"Doctor ID:{doctor_id} logged out.", extra={"method": "DELETE", "statuscode": 200})
        return jsonify({'success': True}), 200
    except Exception as e:
        session.rollback()
        logger.error(f"A log out attempt failed.", extra={"method": "DELETE", "statuscode": 500, "exc": str(e)})
        return jsonify({'error': str(e)}), 500
    finally:
        session.close()