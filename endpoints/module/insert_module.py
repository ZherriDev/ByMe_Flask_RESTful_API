from flask import jsonify, request, Blueprint
from flask_jwt_extended import jwt_required, verify_jwt_in_request, get_jwt_identity
from marshmallow import Schema, fields
from datetime import datetime
from sqlalchemy import text
from ..conn import Session
from ..logger import logger

insert_module_bp = Blueprint('insert_module', __name__)

class InsertModuleSchema(Schema):
    patient_id = fields.Int(required=True)
    episode = fields.String(required=True)
    module = fields.String(required=True)
    status = fields.String(required=True)

@insert_module_bp.route('/insert_module', methods=['POST'])
@jwt_required()
def insert_module():
    
    doctor_id = get_jwt_identity()

    data = request.get_json()
    schema = InsertModuleSchema()
    errors = schema.validate(data)
    
    if errors:
        logger.error(f"Invalid request made by Doctor ID: {doctor_id}", extra={"method": "POST", "statuscode": 400})
        return jsonify({'errors': errors, 'data': data}), 400
    
    session = Session()
    try:
        session.execute(
            text("INSERT INTO modules (patient_id, episode, module, status) VALUES (:patient_id, :episode , :module, :status)"),
            {
                'patient_id': data['patient_id'], 
                'episode': data['episode'],
                'module': data['module'],
                'status': data['status']
            },
            
        )
        session.commit()
        logger.info(f"Doctor ID: {doctor_id} create a Module", extra={"method": "POST", "statuscode": 201})
        return jsonify({'success': True}), 201
    except Exception as e:
        session.rollback()
        logger.warning(str(e), extra={"method": "POST", "statuscode": 500})
        return jsonify({'error': str(e)}), 500
    finally:
        session.close()