from flask import jsonify, request, Blueprint
from flask_jwt_extended import jwt_required, verify_jwt_in_request
from marshmallow import Schema, fields
from sqlalchemy import text
from ..conn import Session

update_doctor_bp = Blueprint('update_doctor', __name__)

class UpdateDoctorSchema(Schema):
    doctor_id = fields.Int(required=True)
    fullname = fields.Str(required=True)
    photo = fields.Str(required=True)
    telephone = fields.Int(required=True)
    sex = fields.Str(required=True)
    birthdate = fields.Date(required=True)
    address = fields.Str(required=True)
    speciality = fields.Str(required=True)

@update_doctor_bp.route('/update_doctor', methods=['PATCH'])
@jwt_required()
def update_doctor():
    
    data = request.get_json()
    schema = UpdateDoctorSchema()
    errors = schema.validate(data)
    
    if errors:
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
        return jsonify({'success': True}), 200
    except Exception as e:
        session.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        session.close()