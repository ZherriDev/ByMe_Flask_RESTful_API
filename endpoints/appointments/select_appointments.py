from flask import jsonify, request, Blueprint
from flask_jwt_extended import jwt_required, verify_jwt_in_request
from marshmallow import Schema, fields
from sqlalchemy import text
from ..conn import Session
from ..logger import logger

select_appointments_bp = Blueprint('select_appointments', __name__)

class SelectAppointmentSchema(Schema):
    date = fields.Str(required=True)

@select_appointments_bp.route("/select_appointments/<query>/<date>", methods=['GET'])
@jwt_required()
def select_appointments(query, date):
    data = {'date': date}
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
                text("SELECT * FROM appointments WHERE date = ':date'"),
                {'date': date}
            ).fetchall()
        elif query == 'all':
            result = session.execute(
                text("SELECT * FROM appointments WHERE date >= ':date'"),
                {'date': date}
            ).fetchall()
        
        for appointment in result:
            appointment = appointment._asdict()
            appointments.append(appointment)
        
        logger.info(f"Selection of {data['date']} done successfully.", extra={"method": "GET", "statuscode": 200})
        return jsonify({'success': True, 'appointments': appointments}), 200
    except Exception as e:
        session.rollback()
        logger.error(f"An attempt to select {data['date']} failed.", extra={"method": "GET", "statuscode": 500, "exc": str(e)})
        return jsonify({'error': str(e)}), 500
    finally:
        session.close()
