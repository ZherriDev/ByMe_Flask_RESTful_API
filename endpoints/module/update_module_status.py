from flask import jsonify, request, Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import Schema, fields
from sqlalchemy import text
from ..conn import Session
from ..logger import logger
from ..utils import limiter

update_module_status_bp = Blueprint('update_module_status', __name__)

class UpdateModuleStatusSchema(Schema):
    module_id = fields.Int(required=True)
    status = fields.Str(required=True)

@update_module_status_bp.route('/update_module_status', methods=['PATCH'])
@jwt_required()
@limiter.limit("5 per minute")
def update_module():
    doctor_id = get_jwt_identity()

    data = request.get_json()
    schema = UpdateModuleStatusSchema()
    errors = schema.validate(data)

    if errors:
        logger.error(f"Invalid module status update request made by Doctor ID:{doctor_id}.", extra={"method": "PATCH", "statuscode": 400})
        return jsonify({'errors': errors}), 400
    
    session = Session()
    
    module_id = data['module_id']
    
    try:
        session.execute(
            text('UPDATE modules SET status = :status WHERE module_id = :module_id'),
            {
                'status': data['status'],
                'module_id': module_id,
            }
        )
        session.commit()
        
        logger.info(f"Doctor ID:{doctor_id} updated status of Module ID:{module_id}.", extra={"method": "PATCH", "statuscode": 200})
        return jsonify({'success': True}), 200
    except Exception as e:
        session.rollback()
        logger.error(f"Doctor ID:{doctor_id}'s attempt to update Module ID:{module_id} status failed.", extra={"method": "PATCH", "statuscode": 500, "exc": str(e)})
        return jsonify({'error': str(e)}), 500
    finally:
        session.close()
