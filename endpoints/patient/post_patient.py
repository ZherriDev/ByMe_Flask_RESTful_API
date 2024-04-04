from flask import jsonify, request, Blueprint
from marshmallow import Schema, fields
from datetime import datetime
from sqlalchemy import text
from ..conn import Session

post_patient_bp = Blueprint('post_patient', __name__)

class InsertPatientSchema(Schema):
    doctor_id = fields.Int(required=True)
    name = fields.Str(required=True)
    telephone = fields.Int(required=True)
    email = fields.Str(required=True)
    sex = fields.Str(required=True)
    birthdate = fields.Date(required=True)
    processnumber = fields.Int(required=True)
    address = fields.Str(required=True)
    postalcode = fields.Str(required=True)
    town = fields.Str(required=True)
    nif = fields.Int(required=True)
    sns = fields.Int(required=True)

@post_patient_bp.route('/insert_patient', methods=['POST'])
def insert_patient():
    data = request.get_json()
    schema = InsertPatientSchema()
    errors = schema.validate(data)

    if errors:
        return jsonify({'errors': errors}), 400
    
    session = Session()
    try:
        session.execute(
            text("INSERT INTO patients (name, telephone, email, sex, birthdate, address, postalcode, town, nif, \
                sns, doctor_id, processnumber, admission_date) VALUES (:name, :telephone, :email, :sex, :birthdate, :address, :postcode, \
                :town, :nif, :sns, :doctor_id, :processnumber, :admission_date)"),
            {
                'name': data['name'], 
                'telephone': data['telephone'],
                'email': data['email'],
                'sex': data['sex'], 
                'birthdate': data['birthdate'], 
                'address': data['address'], 
                'postalcode': data['postalcode'], 
                'town': data['town'], 
                'nif': data['nif'], 
                'sns':data['sns'],
                'doctor_id': data['doctor_id'],
                'processnumber': data['processnumber'],
                'admission_date': datetime.now()
            },
            
        )
        session.commit()
        return jsonify({'success': True}), 201
    except Exception as e:
        session.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        session.close()