from flask import jsonify, request, Blueprint
from flask_jwt_extended import jwt_required, verify_jwt_in_request
from marshmallow import Schema, fields
from sqlalchemy import text
from ..conn import Session
from ..logger import logger
from ..utils import limiter

update_doctor_bp = Blueprint('update_doctor', __name__)

class UpdateDoctorSchema(Schema):
    doctor_id = fields.Int(required=True)
    fullname = fields.Str(required=True)
    photo = fields.Str(required=True)
    telephone = fields.Int(allow_none=True)
    sex = fields.Str(allow_none=True)
    birthdate = fields.String(allow_none=True)
    address = fields.Str(allow_none=True)
    speciality = fields.Str(required=True)

@update_doctor_bp.route('/update_doctor', methods=['PATCH'])
@jwt_required()
@limiter.limit("5 per minute")
def update_doctor():
    
    data = request.get_json()
    schema = UpdateDoctorSchema()
    errors = schema.validate(data)
    
    if errors:
        logger.error(f"Invalid update doctor request made", extra={"method": "PATCH", "statuscode": 400})
        return jsonify({'errors': errors}), 400
    
    session = Session()
    
    try:
        result = session.execute(
            text('UPDATE doctors SET fullname = :fullname, photo = :photo, telephone = :telephone, sex = :sex, \
                birthdate = :birthdate, address = :address, speciality = :speciality WHERE doctor_id = :id'),
            {
                'fullname': data['fullname'], 
                'photo': data['photo'],
                'telephone': data['telephone'], 
                'sex': data['sex'], 
                'birthdate': data['birthdate'], 
                'address': data['address'], 
                'speciality': data['speciality'], 
                'id': data['doctor_id']
            }
        )
        session.commit()
        
        logger.info(f"Doctor ID:{data['doctor_id']} made an update to his profile.", extra={"method": "PATCH", "statuscode": 200})
        return jsonify({'success': True}), 200
    except Exception as e:
        session.rollback()
        logger.error(f"An attempt to update Doctor ID:{data['doctor_id']} profile failed.", extra={"method": "PATCH", "statuscode": 500, "exc": str(e)})
        return jsonify({'error': str(e)}), 500
    finally:
        session.close()
