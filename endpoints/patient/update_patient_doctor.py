from flask import jsonify, request, Blueprint
from flask_jwt_extended import jwt_required, verify_jwt_in_request
from marshmallow import Schema, fields
from datetime import datetime
from sqlalchemy import text
from ..conn import Session

update_patient_doctor_bp = Blueprint('update_patient_doctor', __name__)

class UpdatePatientDoctorSchema(Schema):
    patient_id = fields.Int(required=True)
    doctor_id = fields.Int(required=True)

@update_patient_doctor_bp.route('/update_patient_doctor', methods=['PATCH'])
@jwt_required()
def update_patient_doctor():
    
    data = request.get_json()
    schema = UpdatePatientDoctorSchema()
    errors = schema.validate(data)
    
    if errors:
        return jsonify({'errors': errors, 'data': data}), 400
    
    session = Session()
    
    try:
        session.execute(
            text("UPDATE patients SET doctor_id = :doctor_id, admission_date = :admission_date WHERE patient_id = :patient_id"),
            {
                'patient_id': data['patient_id'],
                'doctor_id': data['doctor_id'],
                'admission_date': datetime.now()
            },
            
        )
        session.commit()
        return jsonify({'success': True}), 201
    except Exception as e:
        session.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        session.close()