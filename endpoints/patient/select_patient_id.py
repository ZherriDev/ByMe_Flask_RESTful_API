from flask import jsonify, request, Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import Schema, fields
from sqlalchemy import text
from ..conn import Session
from ..logger import logger

select_patient_id_bp = Blueprint('select_patient', __name__)

class SelectPatientSchema(Schema):
    patient_id = fields.Int(required=True)

@select_patient_id_bp.route('/select_patient/<int:id>', methods=['GET'])
@jwt_required()
def select_patient(id):
    
    doctor_id = get_jwt_identity()
    
    data = {'patient_id': id}
    schema = SelectPatientSchema()
    errors = schema.validate(data)

    if errors:
        logger.error(f"Invalid patient select request made by Doctor ID:{doctor_id}.", extra={"method": "GET", "statuscode": 400})
        return jsonify({'errors': errors}), 400
        
    session = Session()
    
    try:
        result = session.execute(
            text('SELECT * FROM patients WHERE patient_id = :patient_id'),
            {'patient_id': data['patient_id']}
        ).fetchone()
        
        if result:
            result = result._asdict()
            result['birthdate'] = result['birthdate'].strftime('%Y-%m-%d')
            result['admission_date'] = result['admission_date'].strftime('%Y-%m-%d')
        
        logger.info(f"Selection of Patient ID:{data['patient_id']} done successfully.", extra={"method": "GET", "statuscode": 200})
        return jsonify({'success': True, 'patient': result}), 200
    except Exception as e:
        session.rollback()
        logger.error(f"Doctor ID:{doctor_id}'s attempt to select Patient ID:{data['patient_id']} failed.", extra={"method": "GET", "statuscode": 500, "exc": str(e)})
        return jsonify({'error': str(e)}), 500
    finally:
        session.close()