from flask import jsonify, request, Blueprint
from flask_jwt_extended import jwt_required
from marshmallow import Schema, fields
from sqlalchemy import text
from datetime import datetime
from ..conn import Session
from ..logger import logger
from ..utils import limiter

insert_appointments_bp = Blueprint('insert_appointments', __name__)

class InsertAppointmentSchema(Schema):
    doctor_id = fields.Int(required=True)
    patient_id = fields.Int(required=True)
    subject = fields.Str(required=True)
    date = fields.Str(required=True)
    time = fields.Str(required=True)

@insert_appointments_bp.route('/insert_appointments', methods=['POST'])
@limiter.limit("5 per minute")
@jwt_required()
def insert_appointments():
    data = request.get_json()
    schema = InsertAppointmentSchema()
    errors = schema.validate(data)
    
    if errors:
        logger.error(f"Invalid appointment insert request made by Doctor ID:{data['doctor_id']}.", extra={"method": "POST", "statuscode": 400})
        return jsonify({'errors': errors}), 400
    
    session = Session()
    
    try:
        session.execute(
            text('INSERT INTO appointments (doctor_id, patient_id, subject, date, time) VALUES (:doctor_id, :patient_id, :subject, :date, :time)'),
            {
                'doctor_id': data['doctor_id'],
                'patient_id': data['patient_id'],
                'subject': data['subject'],
                'date': data['date'],
                'time': data['time'],
            }
        )
        session.commit()
        
        appointment_id = session.execute(text("SELECT LAST_INSERT_ID()")).scalar()
    
        logger.info(f"Doctor ID:{data['doctor_id']} added a Appointment ID:{appointment_id} with Patient ID:{data['patient_id']}.", extra={"method": "POST", "statuscode": 201})
        return jsonify({'success': True}), 201
    except Exception as e:
        session.rollback()
        logger.error(f"Doctor ID:{data['doctor_id']}'s attempt to insert a Appointment with Patient ID:{data['patient_id']} failed.", extra={"method": "POST", "statuscode": 500, "exc": str(e)})
        return jsonify({'error': str(e)}), 500
    finally:
        session.close()
