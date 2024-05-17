from flask import jsonify, request, Blueprint
from flask_jwt_extended import jwt_required, verify_jwt_in_request
from marshmallow import Schema, fields
from sqlalchemy import text
from ..conn import Session
from ..logger import logger

select_doctors_bp = Blueprint('select_doctors', __name__)

class SelectDoctorsSchema(Schema):
    search = fields.Str(required=True)

@select_doctors_bp.route('/select_doctors', methods=['GET'], defaults={'search': None})
@select_doctors_bp.route('/select_doctors/<search>', methods=['GET'])
@jwt_required()
def select_doctors(search):
    
    data = {'search': search}
    schema = SelectDoctorsSchema()
    errors = schema.validate(data)

    if errors:
        logger.error(f"Invalid select doctors request made", extra={"method": "GET", "statuscode": 400})
        return jsonify({'errors': errors}), 400
    
    session = Session()
    
    try:
        doctors = []
        if data['search']:
            result = session.execute(
                text('SELECT * FROM doctors WHERE fullname LIKE :search OR speciality LIKE :search ORDER BY fullname'),
                {'search': "%" + data['search'] + "%"}
            ).fetchall()
        else:
            result = session.execute(
                text('SELECT * FROM doctors ORDER BY fullname'),
            ).fetchall()
            
        for doctor in result:
            doctor = doctor._asdict()
            doctor['birthdate'] = doctor['birthdate'].strftime('%Y-%m-%d')
            doctors.append(doctor)
        
        logger.info(f"Selection of {data['search']} done successfully.", extra={"method": "GET", "statuscode": 200})
        return jsonify({'success': True, 'doctors': doctors}), 200
    except Exception as e:
        session.rollback()
        logger.error(f"An attempt to select {data['search']} failed.", extra={"method": "GET", "statuscode": 500, "exc": str(e)})
        return jsonify({'error': str(e)}), 500
    finally:
        session.close()
