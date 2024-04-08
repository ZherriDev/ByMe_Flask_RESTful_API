from flask import jsonify, request, Blueprint
from flask_jwt_extended import jwt_required
from marshmallow import Schema, fields
from sqlalchemy import text
from ..conn import Session

select_doctor_bp = Blueprint('select_doctor', __name__)

class SelectDoctorSchema(Schema):
    search = fields.Str(required=True)

@select_doctor_bp.route('/select_doctor', methods=['POST'])
@jwt_required()
def select_doctor():
    data = request.get_json()
    schema = SelectDoctorSchema()
    errors = schema.validate(data)

    if errors:
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
            doctors.append(doctor)
        return jsonify({'success': True, 'doctors': doctors}), 200
    except Exception as e:
        session.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        session.close()