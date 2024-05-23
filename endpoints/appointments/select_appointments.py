from flask import jsonify, request, Blueprint
from flask_jwt_extended import jwt_required, verify_jwt_in_request
from marshmallow import Schema, fields
from sqlalchemy import text
from datetime import datetime
from ..conn import Session
from ..logger import logger

select_appointments_bp = Blueprint('select_appointments', __name__)

class SelectAppointmentSchema(Schema):
    date = fields.Str(required=True)
    time = fields.Str(required=True)

@select_appointments_bp.route("/select_appointments/<query>/<date>/<time>", methods=['GET'])
@jwt_required()
def select_appointments(query, date, time):
    data = {'date': date, 'time': time}
    schema = SelectAppointmentSchema()
    errors = schema.validate(data)

    if errors:
        logger.error(f"Invalid select appointments request made", extra={"method": "GET", "statuscode": 400})
        return jsonify({'errors': errors}), 400
    
    session = Session()
    
    try:
        appointments = []

        if query == 'one':
            result = session.execute(
                text('SELECT * FROM appointments WHERE date = :date AND time >= :time ORDER BY time ASC'),
                {'date': date, 'time': time}
            ).fetchall()
        elif query == 'all':
            result = session.execute(
                text('SELECT * FROM appointments WHERE date >= :date ORDER BY date ASC'),
                {'date': date}
            ).fetchall()
        
        for appointment in result:
            appointment = appointment._asdict()
            appointment['date'] = appointment['date'].strftime('%Y-%m-%d')
            hours, remainder = divmod(appointment['time'].seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            appointment['time'] = '{:02}:{:02}:{:02}'.format(hours, minutes, seconds)
            result2 = session.execute(
                text('SELECT name, processnumber FROM patients WHERE patient_id = :patient_id'),
                {'patient_id': appointment['patient_id']}
            ).fetchone()
            appointment['patient_data'] = {
                'name': result2[0],
                'processnumber': result2[1]
            }
            if query == 'all':
                if appointment['date'] == date:
                    if appointment['time'] >= time:
                        appointments.append(appointment)
                    else:
                        pass
                else:
                    appointments.append(appointment)
            else:
                appointments.append(appointment)
        
        logger.info(f"Selection of {data['date']} done successfully.", extra={"method": "GET", "statuscode": 200})
        return jsonify({'success': True, 'appointments': appointments}), 200
    except Exception as e:
        session.rollback()
        logger.error(f"An attempt to select {data['date']} failed.", extra={"method": "GET", "statuscode": 500, "exc": str(e)})
        return jsonify({'error': str(e)}), 500
    finally:
        session.close()
