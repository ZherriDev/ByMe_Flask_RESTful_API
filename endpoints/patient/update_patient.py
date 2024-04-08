from flask import jsonify, request, Blueprint
from flask_jwt_extended import jwt_required
from marshmallow import Schema, fields
from sqlalchemy import text
from ..conn import Session

update_patient_bp = Blueprint('update_patient', __name__)

class UpdatePatientSchema(Schema):
    patient_id = fields.Int(required=True)
    doctor_id = fields.Int(required=True)
    name = fields.Str(required=True)
    telephone = fields.Int(required=True)
    email = fields.Str(required=True)
    sex = fields.Str(required=True)
    birthdate = fields.Date(required=True)
    address = fields.Str(required=True)
    postalcode = fields.Str(required=True)
    town = fields.Str(required=True)
    nif = fields.Int(required=True)
    sns = fields.Int(required=True)
    
@update_patient_bp.route('/update_patient', methods=['PATCH'])
@jwt_required()
def update_patient():
    data = request.get_json()
    schema = UpdatePatientSchema()
    errors = schema.validate(data)

    if errors:
        return jsonify({'errors': errors}), 400
    
    session = Session()
    
    try:
        
        session.execute(
            text('UPDATE patients SET doctor_id = :doctor_id, name = :name, telephone = :telephone, email = :email, \
                sex = :sex, birthdate = :birthdate, address = :address, \
                postalcode = :postalcode, town = :town, nif = :nif, sns = :sns WHERE patient_id = :patient_id'),
            {
                'doctor_id': data['doctor_id'], 
                'name': data['name'], 
                'telephone': data['telephone'], 
                'email': data['email'],
                'sex': data['sex'], 
                'birthdate': data['birthdate'], 
                'address': data['address'],
                'postalcode': data['postalcode'], 
                'town': data['town'], 
                'nif': data['nif'], 
                'sns': data['sns'], 
                'patient_id': data['patient_id'],
            }
        )
        session.commit()
        return jsonify({'success': True}), 200
    except Exception as e:
        session.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        session.close()