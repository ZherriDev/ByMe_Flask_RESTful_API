from flask import jsonify, request, Blueprint
from flask_jwt_extended import jwt_required, verify_jwt_in_request, get_jwt_identity
from marshmallow import Schema, fields
from datetime import datetime
from sqlalchemy import text
from ..conn import Session
from ..logger import logger

insert_patient_bp = Blueprint('insert_patient', __name__)

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

@insert_patient_bp.route('/insert_patient', methods=['POST'])
@jwt_required()
def insert_patient():
    
    doctor_id = get_jwt_identity()

    data = request.get_json()
    schema = InsertPatientSchema()
    errors = schema.validate(data)

    if errors:
        logger.error(f"Invalid request made by Doctor ID: {doctor_id}", extra={"method": "POST", "statuscode": 400})
        return jsonify({'errors': errors}), 400
    
    session = Session()
    try:
        session.execute(
            text("INSERT INTO patients (name, telephone, email, sex, birthdate, address, postalcode, town, nif, \
                sns, doctor_id, processnumber, admission_date) VALUES (:name, :telephone, :email, :sex, :birthdate, :address, :postalcode, \
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
        logger.info(f"Doctor ID: {doctor_id} created a new Patient", extra={"method": "POST", "statuscode": 201})
        return jsonify({'success': True}), 201
    except Exception as e:
        session.rollback()
        logger.error(f"Doctor ID: {doctor_id} tried to insert Patient", extra={"method": "POST", "statuscode": 500, "exc": str(e)})
        return jsonify({'error': str(e)}), 500
    finally:
        session.close()