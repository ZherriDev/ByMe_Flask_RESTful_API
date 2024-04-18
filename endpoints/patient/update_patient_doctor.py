from flask import jsonify, request, Blueprint
from flask_jwt_extended import jwt_required, verify_jwt_in_request, get_jwt_identity
from marshmallow import Schema, fields
from datetime import datetime
from sqlalchemy import text
from ..conn import Session
from ..logger import logger

update_patient_doctor_bp = Blueprint('update_patient_doctor', __name__)

class UpdatePatientDoctorSchema(Schema):
    patient_id = fields.Int(required=True)
    doctor_id = fields.Int(required=True)

@update_patient_doctor_bp.route('/update_patient_doctor', methods=['PATCH'])
@jwt_required()
def update_patient_doctor():
    
    doctor_id = get_jwt_identity()

    data = request.get_json()
    schema = UpdatePatientDoctorSchema()
    errors = schema.validate(data)
    
    if errors:
        logger.error(f"Invalid request made by Doctor ID: {doctor_id}", extra={"method": "PATCH", "statuscode": 400})
        return jsonify({'errors': errors, 'data': data}), 400
    
    session = Session()
    new_doctor_id = data['doctor_id']
    patient_id = data['patient_id']
    
    try:
        session.execute(
            text("UPDATE patients SET doctor_id = :doctor_id, admission_date = :admission_date WHERE patient_id = :patient_id"),
            {
                'patient_id': patient_id,
                'doctor_id': new_doctor_id,
                'admission_date': datetime.now()
            },
            
        )
        session.commit()
        logger.info(f"Doctor ID: {doctor_id} updated new Doctor ID: {new_doctor_id} of Patiend ID: {patient_id}", extra={"method": "PATCH", "statuscode": 200})
        return jsonify({'success': True}), 200
    except Exception as e:
        session.rollback()
        logger.error(f"Doctor ID: {doctor_id} tried to update New Doctor ID: {new_doctor_id} from Patient ID: {patient_id}", extra={"method": "PATCH", "statuscode": 500, "exc": str(e)})
        return jsonify({'error': str(e)}), 500
    finally:
        session.close()