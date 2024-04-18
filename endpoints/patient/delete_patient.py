from flask import jsonify, request, Blueprint
from flask_jwt_extended import jwt_required, verify_jwt_in_request, get_jwt_identity
from marshmallow import Schema, fields
from sqlalchemy import text
from ..conn import Session
from ..logger import logger

delete_patient_bp = Blueprint('delete_patient_bp', __name__)

class DeletePatientSchema(Schema):
    patient_id = fields.Int(required=True)

@delete_patient_bp.route('/delete_patient', methods=['DELETE'])
@jwt_required()
def delete_patient():
    
    doctor_id = get_jwt_identity()

    data = request.get_json()
    schema = DeletePatientSchema()
    errors = schema.validate(data)

    if errors:
        logger.error(f"Invalid request made by Doctor ID: {doctor_id}", extra={"method": "DELETE", "statuscode": 400})
        return jsonify({'errors': errors}), 400
    
    session = Session()
    patient_id = data['patient_id']
    
    try:
        session.execute(
            text("DELETE FROM patients WHERE patient_id = :id"),
            {'id': data['patient_id']},
        )
        session.commit()
        logger.info(f"Doctor ID: {doctor_id} deleted Patient ID: {patient_id}", extra={"method": "DELETE", "statuscode": 200})
        return jsonify({'success': True}), 200
    except Exception as e:
        session.rollback()
        logger.error(f"Doctor ID: {doctor_id} tried to delete Patient ID: {patient_id}", extra={"method": "DELETE", "statuscode": 500, "exc": str(e)})
        return jsonify({'error': str(e)}), 500
    finally:
        session.close()