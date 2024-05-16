from flask import jsonify, request, Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import Schema, fields
from sqlalchemy import text
from ..conn import Session
from ..logger import logger

delete_session_bp = Blueprint('delete_session_bp', __name__)

class DeleteSessionSchema(Schema):
    session_id = fields.Int(required=True)

@delete_session_bp.route('/delete_session', methods=['DELETE'])
@jwt_required()
def delete_patient():
    
    doctor_id = get_jwt_identity()

    data = request.get_json()
    schema = DeleteSessionSchema()
    errors = schema.validate(data)

    if errors:
        logger.error(f"Invalid session delete request made by Doctor ID:{doctor_id}.", extra={"method": "DELETE", "statuscode": 400})
        return jsonify({'errors': errors}), 400
    
    session = Session()
    session_id = data['session_id']
    
    try:
        session.execute(
            text("DELETE FROM session WHERE session_id = :id"),
            {'id': session_id}
        )
        session.commit()
        
        session.execute(
            text("DELETE FROM patients WHERE patient_id = :id"),
            {'id': data['patient_id']},
        )
        session.commit()
        
        logger.info(f"Doctor ID:{doctor_id} deleted Patient ID:{patient_id}.", extra={"method": "DELETE", "statuscode": 200})
        return jsonify({'success': True}), 200
    except Exception as e:
        session.rollback()
        logger.error(f"Doctor ID:{doctor_id}'s attempt to delete Patient ID:{patient_id} failed.", extra={"method": "DELETE", "statuscode": 500, "exc": str(e)})
        return jsonify({'error': str(e)}), 500
    finally:
        session.close()