from flask import jsonify, request, Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import Schema, fields
from sqlalchemy import text
from ..conn import Session
from ..logger import logger

delete_appointments_bp = Blueprint('delete_appointments', __name__)

class DeleteAppointmentsSchema(Schema):
    appointment_id = fields.Int(required=True)
    
@delete_appointments_bp.route('/delete_appointment', methods=['DELETE'])
@jwt_required()
def delete_appointment():
    
    doctor_id = get_jwt_identity()
    
    data = request.get_json()
    schema = DeleteAppointmentsSchema()
    errors = schema.validate(data)
    
    if errors:
        logger.error(f"Invalid delete appointment request made", extra={"method": "DELETE", "statuscode": 400})
        return jsonify({'errors': errors}), 400
    
    session = Session()
    
    try:
        appointment_id = data['appointment_id']
        session.execute(text('DELETE FROM appointments WHERE appointment_id = :appointment_id'),
            {
                'appointment_id': appointment_id,
            },
            )
        session.commit()
        logger.info(f"Doctor ID:{doctor_id} deleted Appointment ID:{appointment_id}", extra={"method": "DELETE", "statuscode": 200})
        return jsonify({'succes': True}), 200
    except Exception as e:
        session.rollback()
        logger.error(f"Doctor ID:{doctor_id}'s attempt to delete Appointment ID:{appointment_id} failed.", extra={"method": "DELETE", "statuscode": 500, "exc": str(e)})      
        return jsonify({'error': str(e)}), 500
    finally:
        session.close()