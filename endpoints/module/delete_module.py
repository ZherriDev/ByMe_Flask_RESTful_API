from flask import jsonify, request, Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import Schema, fields
from sqlalchemy import text
from ..conn import Session
from ..logger import logger

delete_module_bp = Blueprint('delete_module', __name__)

class DeleteModuleSchema(Schema):
    module_id = fields.Int(required=True)

@delete_module_bp.route('/delete_module', methods=['DELETE'])
@jwt_required()
def delete_module():

    doctor_id = get_jwt_identity()

    data = request.get_json()
    schema = DeleteModuleSchema()
    errors = schema.validate(data)

    if errors:
        logger.error(f"Invalid module delete request made by Doctor ID: {doctor_id}.", extra={"method": "DELETE", "statuscode": 400})
        return jsonify({'errors': errors}), 400
    
    session = Session()
    module_id = data['module_id']
    
    try:
        session.execute(
            text("DELETE FROM modules WHERE module_id = :id"),
            {'id': module_id},
        )
        session.commit()
        
        logger.info(f"Doctor ID:{doctor_id} deleted Module ID:{module_id}.", extra={"method": "DELETE", "statuscode": 200})
        return jsonify({'success': True}), 200
    except Exception as e:
        session.rollback()
        logger.error(f"Doctor ID:{doctor_id}'s attempt to delete Module ID:{module_id} failed.", extra={"method": "DELETE", "statuscode": 500, "exc": str(e)})
        return jsonify({'error': str(e)}), 500
    finally:
        session.close()