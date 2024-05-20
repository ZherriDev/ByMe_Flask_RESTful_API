from flask import jsonify, request, Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import Schema, fields
from sqlalchemy import text
from ..conn import Session
from ..logger import logger
from ..utils import limiter

update_patient_status_bp = Blueprint('update_patient_status', __name__)

class UpdatePatientStatusSchema(Schema):
    patient_id = fields.Int(required=True)
    status = fields.Str(required=True)

@update_patient_status_bp.route('/update_patient_status', methods=['PATCH'])
@jwt_required()
@limiter.limit("5 per minute")
def update_patient():
    doctor_id = get_jwt_identity()

    data = request.get_json()
    schema = UpdatePatientStatusSchema()
    errors = schema.validate(data)

    if errors:
        logger.error(f"Invalid patient status update request made by Doctor ID:{doctor_id}.", extra={"method": "PATCH", "statuscode": 400})
        return jsonify({'errors': errors}), 400
    
    session = Session()
    
    patient_id = data['patient_id']
    
    try:
        session.execute(
            text('UPDATE patients SET status = :status WHERE patient_id = :patient_id'),
            {
                'status': data['status'],
                'patient_id': patient_id,
            }
        )
        session.commit()
        
        logger.info(f"Doctor ID:{doctor_id} updated status of Patient ID:{patient_id}.", extra={"method": "PATCH", "statuscode": 200})
        return jsonify({'success': True}), 200
    except Exception as e:
        session.rollback()
        logger.error(f"Doctor ID:{doctor_id}'s attempt to update Patient ID:{patient_id} status failed.", extra={"method": "PATCH", "statuscode": 500, "exc": str(e)})
        return jsonify({'error': str(e)}), 500
    finally:
        session.close()
