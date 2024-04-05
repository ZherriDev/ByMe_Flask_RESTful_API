from flask import jsonify, request, Blueprint
from marshmallow import Schema, fields
from sqlalchemy import text
from ..conn import Session

select_doctor_id_bp = Blueprint('select_doctor_id', __name__)

class SelectDoctorIDSchema(Schema):
    doctor_id = fields.Int(required=True)

@select_doctor_id_bp.route('/select_doctor_id', methods=['POST'])
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
        ).fetchone()
        if result:
            result = result._asdict()
        return jsonify({'success': True, 'doctor': result}), 200
    except Exception as e:
        session.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        session.close()