from flask import jsonify, request, Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import Schema, fields
from datetime import datetime
from sqlalchemy import text
from ..conn import Session
from ..logger import logger
from ..utils import limiter

insert_module_bp = Blueprint('insert_module', __name__)

class InsertModuleSchema(Schema):
    patient_id = fields.Int(required=True)
    episode = fields.String(required=True)
    module = fields.String(required=True)
    status = fields.String(required=True)

@insert_module_bp.route('/insert_module', methods=['POST'])
@limiter.limit("5 per minute")
@jwt_required()
def insert_module():
    
    doctor_id = get_jwt_identity()

    data = request.get_json()
    schema = InsertModuleSchema()
    errors = schema.validate(data)
    
    if errors:
        logger.error(f"Invalid module insert request made by Doctor ID:{doctor_id}.", extra={"method": "POST", "statuscode": 400})
        return jsonify({'errors': errors}), 400
    
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
        
        module_id = session.execute("SELECT last_insert_rowid()").scalar()
        
        logger.info(f"Doctor ID:{doctor_id} added a Module ID:{module_id} to Patient ID:{data['patient_id']}.", extra={"method": "POST", "statuscode": 201})
        return jsonify({'success': True}), 201
    except Exception as e:
        session.rollback()
        logger.error(f"Doctor ID:{doctor_id}'s attempt to insert a Module to Patient ID:{data['patient_id']} failed.", extra={"method": "POST", "statuscode": 500, "exc": str(e)})
        return jsonify({'error': str(e)}), 500
    finally:
        session.close()