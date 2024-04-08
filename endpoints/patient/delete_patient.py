from flask import jsonify, request, Blueprint
from flask_jwt_extended import jwt_required
from marshmallow import Schema, fields
from sqlalchemy import text
from ..conn import Session

delete_patient_bp = Blueprint('delete_patient_bp', __name__)

class DeletePatientSchema(Schema):
    patient_id = fields.Int(required=True)

@delete_patient_bp.route('/delete_patient', methods=['DELETE'])
@jwt_required()
def delete_patient():
    data = request.get_json()
    schema = DeletePatientSchema()
    errors = schema.validate(data)

    if errors:
        return jsonify({'errors': errors}), 400
    
    session = Session()
    
    try:
        session.execute(
            text("DELETE FROM patients WHERE patient_id = :id"),
            {'id': data['patient_id']},
        )
        session.commit()
        return jsonify({'success': True}), 200
    except Exception as e:
        session.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        session.close()