from flask import jsonify, request, Blueprint
from marshmallow import Schema, fields
from sqlalchemy import text
from ..conn import Session

update_patient_doctor_bp = Blueprint('update_patient_doctor', __name__)

class UpdatePatientDoctorSchema(Schema):
    patient_id = fields.Int(required=True)
    doctor_id = fields.Int(required=True)

@update_patient_doctor_bp.route('/update_patient_doctor', methods=['PATCH'])
def update_patient_doctor():
    data = request.get_json()
    schema = UpdatePatientDoctorSchema()
    errors = schema.validate(data)
    
    if errors:
        return jsonify({'errors': errors, 'data': data}), 400
    
    session = Session()
    
    try:
        session.execute(
            text("UPDATE patients SET doctor_id = :doctor_id WHERE patient_id = :patient_id"),
            {
                'patient_id': data['patient_id'],
                'doctor_id': data['doctor_id']
            },
            
        )
        session.commit()
        return jsonify({'success': True}), 201
    except Exception as e:
        session.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        session.close()