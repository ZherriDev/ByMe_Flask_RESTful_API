from flask import jsonify, request, Blueprint
from marshmallow import Schema, fields
from datetime import datetime
from sqlalchemy import text
from ..conn import Session

update_module_bp = Blueprint('update_module', __name__)

class UpdateModuleSchema(Schema):
    module_id = fields.Int(required=True)
    episode = fields.String(required=True)
    module = fields.String(required=True)
    status = fields.String(required=True)

@update_module_bp.route('/update_module', methods=['PATCH'])
def insert_module():
    data = request.get_json()
    schema = UpdateModuleSchema()
    errors = schema.validate(data)
    
    if errors:
        return jsonify({'errors': errors, 'data': data}), 400
    
    session = Session()
    try:
        session.execute(
            text("UPDATE module SET episode = :episode, module = :module, status = :status WHERE module = :module_id"),
            {
                'module_id': data['module_id'],
                'episode': data['episode'],
                'module': data['module'],
                'status': data['status'],
            },
            
        )
        session.commit()
        return jsonify({'success': True}), 201
    except Exception as e:
        session.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        session.close()