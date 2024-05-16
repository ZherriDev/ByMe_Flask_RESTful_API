from flask import jsonify, request, Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import Schema, fields
from sqlalchemy import text
from ..conn import Session
from ..logger import logger

update_session_bp = Blueprint('update_session_bp', __name__)

class UpdateSessionSchema(Schema):
    session_id = fields.Int(required=True)

@update_session_bp.route('/update_session', methods=['PATCH'])
@jwt_required()
def update_session():
    
    doctor_id = get_jwt_identity()

    data = request.get_json()
    schema = UpdateSessionSchema()
    errors = schema.validate(data)

    if errors:
        logger.error(f"Invalid session update request made by Doctor ID:{doctor_id}.", extra={"method": "PATCH", "statuscode": 400})
        return jsonify({'errors': errors}), 400
    
    session = Session()
    session_id = data['session_id']
    
    try:
        session.execute(
            text("UPDATE sessions SET in_blacklist = 1 WHERE session_id = :session_id"),
            {'session_id': session_id}
        )
        session.commit()
    
        logger.info(f"Doctor ID:{doctor_id} updated Session ID:{session_id}.", extra={"method": "PATCH", "statuscode": 200})
        return jsonify({'success': True}), 200
    except Exception as e:
        session.rollback()
        logger.error(f"Doctor ID:{doctor_id}'s attempt to update Session ID:{session_id} failed.", extra={"method": "PATCH", "statuscode": 500, "exc": str(e)})
        return jsonify({'error': str(e)}), 500
    finally:
        session.close()