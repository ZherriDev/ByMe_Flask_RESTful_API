from flask import jsonify, request, Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import Schema, fields
from sqlalchemy import text
from ..conn import Session
from ..logger import logger

update_module_bp = Blueprint('update_module', __name__)

class UpdateModuleSchema(Schema):
    module_id = fields.Int(required=True)
    episode = fields.String(required=True)
    module = fields.String(required=True)
    status = fields.String(required=True)

@update_module_bp.route('/update_module', methods=['PATCH'])
@jwt_required()
def update_module():
    
    doctor_id = get_jwt_identity()

    data = request.get_json()
    schema = UpdateModuleSchema()
    errors = schema.validate(data)
    
    if errors:
        logger.error(f"Invalid module update request made by Doctor ID:{doctor_id}.", extra={"method": "PATCH", "statuscode": 400})
        return jsonify({'errors': errors}), 400
    
    session = Session()
    module_id = data['module_id']
    
    try:
        session.execute(
            text("UPDATE modules SET episode = :episode, module = :module, status = :status WHERE module_id = :module_id"),
            {
                'module_id': module_id,
                'episode': data['episode'],
                'module': data['module'],
                'status': data['status'],
            },
            
        )
        session.commit()
        
        logger.info(f"Doctor ID:{doctor_id} updated Module ID:{module_id}.", extra={"method": "PATCH", "statuscode": 200})
        return jsonify({'success': True}), 200
    except Exception as e:
        session.rollback()
        logger.error(f"Doctor ID:{doctor_id}'s attempt to update Module ID:{module_id} failed.", extra={"method": "GET", "statuscode": 500, "exc": str(e)})
        return jsonify({'error': str(e)}), 500
    finally:
        session.close()