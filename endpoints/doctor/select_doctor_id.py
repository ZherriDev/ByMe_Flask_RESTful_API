from flask import jsonify, request, Blueprint
from flask_jwt_extended import jwt_required, verify_jwt_in_request
from marshmallow import Schema, fields
from sqlalchemy import text
from ..conn import Session
from ..logger import logger

select_doctor_id_bp = Blueprint('select_doctor_id', __name__)

class SelectDoctorIDSchema(Schema):
    doctor_id = fields.Int(required=True)

@select_doctor_id_bp.route('/select_doctor/<int:id>', methods=['GET'])
@jwt_required()
def select_doctor_id(id):
    
    data = jsonify({'doctor_id': id})
    schema = SelectDoctorIDSchema()
    errors = schema.validate(data)

    if errors:
        logger.error(f"Invalid select doctor request made", extra={"method": "GET", "statuscode": 400})
        return jsonify({'errors': errors}), 400
    
    session = Session()
    
    try:
        result = session.execute(
            text('SELECT * FROM doctors WHERE doctor_id = :doctor_id'),
            {'doctor_id': data['doctor_id']}
        ).fetchone()
        
        if result:
            result = result._asdict()
        
        logger.info(f"Selection of Doctor ID:{data['doctor_id']} done successfully.", extra={"method": "GET", "statuscode": 200})
        return jsonify({'success': True, 'doctor': result}), 200
    except Exception as e:
        session.rollback()
        logger.error(f"An attempt to select Doctor ID:{data['doctor_id']} failed.", extra={"method": "GET", "statuscode": 500, "exc": str(e)})
        return jsonify({'error': str(e)}), 500
    finally:
        session.close()