from flask import jsonify, request, Blueprint
from marshmallow import Schema, fields
from sqlalchemy import text
from ..conn import Session

delete_doctor_bp = Blueprint('delete_doctor', __name__)

class DeleteDoctorSchema(Schema):
    doctor_id = fields.Int(required=True)

@delete_doctor_bp.route('/delete_doctor', methods=['DELETE'])
def delete_doctor():
    data = request.get_json()
    schema = DeleteDoctorSchema()
    errors = schema.validate(data)

    if errors:
        return jsonify({'errors': errors}), 400
    
    session = Session()
    
    try:
        session.execute(
            text("DELETE FROM doctors WHERE doctor_id = :id"),
            {'id': data['doctor_id']},
        )
        session.commit()
        return jsonify({'success': True}), 200
    except Exception as e:
        session.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        session.close()