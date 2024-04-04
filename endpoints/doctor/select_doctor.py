from flask import jsonify, request, Blueprint
from marshmallow import Schema, fields
from sqlalchemy import text
from ..conn import Session

select_doctor_bp = Blueprint('select_doctor', __name__)

class SelectDoctorSchema(Schema):
    search = fields.Str(required=True)

@select_doctor_bp.route('/select_doctor', methods=['POST'])
def select_doctor():
    data = request.get_json()
    schema = SelectDoctorSchema()
    errors = schema.validate(data)

    if errors:
        return jsonify({'errors': errors}), 400
    
    session = Session()
    
    try:
        result = session.execute(
            text('SELECT * FROM doctors WHERE fullname LIKE "%:search%" OR speciality LIKE "%:search%" ORDER BY name ASC'),
            {'search': data['search']}
        ).fetchall()
        return jsonify({'success': True, 'doctors': result}), 200
    except Exception as e:
        session.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        session.close()