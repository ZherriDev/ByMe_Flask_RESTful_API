from flask import jsonify, request, Blueprint
from flask_jwt_extended import jwt_required, verify_jwt_in_request
from marshmallow import Schema, fields
from sqlalchemy import text
from ..conn import Session

update_module_bp = Blueprint('update_module', __name__)

class UpdateModuleSchema(Schema):
    module_id = fields.Int(required=True)
    episode = fields.String(required=True)
    module = fields.String(required=True)
    status = fields.String(required=True)

@update_module_bp.route('/update_module', methods=['PATCH'])
@jwt_required()
def update_module():
    token = verify_jwt_in_request()
    if not token['fresh']:
        return jsonify({'error': 'Expired token'})
    
    data = request.get_json()
    schema = UpdateModuleSchema()
    errors = schema.validate(data)
    
    if errors:
        return jsonify({'errors': errors, 'data': data}), 400
    
    session = Session()
    try:
        session.execute(
            text("UPDATE modules SET episode = :episode, module = :module, status = :status WHERE module_id = :module_id"),
            {
                'module_id': data['module_id'],
                'episode': data['episode'],
                'module': data['module'],
                'status': data['status'],
            },
            
        )
        session.commit()
        return jsonify({'success': True}), 200
    except Exception as e:
        session.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        session.close()