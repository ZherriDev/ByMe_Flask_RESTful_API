from flask import jsonify, request, Blueprint
from marshmallow import Schema, fields
from sqlalchemy import text
from ..conn import Session

get_doctor_id_bp = Blueprint('get_doctor_id', __name__)

class SelectDoctorIDSchema(Schema):
    doctor_id = fields.Int(required=True)

@get_doctor_id_bp.route('/select_doctor_id', methods=['GET'])
def select_doctor_id():
    data = request.get_json()
    schema = SelectDoctorIDSchema()
    errors = schema.validate(data)

    if errors:
        return jsonify({'errors': errors}), 400
    
    session = Session()
    
    try:
        result = session.execute(
            text('SELECT * FROM doctors WHERE doctor_id = :doctor_id'),
            {'doctor_id': data['doctor_id']}
        ).fetchall()
        return jsonify({'success': True, 'doctor': result}), 200
    except Exception as e:
        session.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        session.close()