from flask import jsonify, request, Blueprint
from marshmallow import Schema, fields
from sqlalchemy import text
from ..conn import Session

update_doctor_bp = Blueprint('update_doctor', __name__)

class UpdateDoctorSchema(Schema):
    id = fields.Int(required=True)
    fullname = fields.Str(required=True)
    telephone = fields.Int(required=True)
    sex = fields.Str(required=True)
    birthdate = fields.Date(required=True)
    address = fields.Str(required=True)
    speciality = fields.Str(required=True)

@update_doctor_bp.route('/update_doctor', methods=['UPDATE'])
def update_doctor():
    data = request.get_json()
    schema = UpdateDoctorSchema()
    errors = schema.validate(data)
    
    if errors:
        return jsonify({'errors': errors}), 400
    
    session = Session()
    
    try:
        result = session.execute(
            text('UPDATE doctors SET fullname = :fullname, telephone = :telephone, sex = :sex, \
                birthdate = :birthdate, address = :address, speciality = :speciality WHERE doctor_id = :id'),
            {
                'fullname': data['fullname'], 
                'telephone': data['telephone'], 
                'sex': data['sex'], 
                'birthdate': data['birthdate'], 
                'address': data['address'], 
                'speciality': data['speciality'], 
                'id': data['id']}
        )
        session.commit()
        return jsonify({'success': True}), 200
    except Exception as e:
        session.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        session.close()