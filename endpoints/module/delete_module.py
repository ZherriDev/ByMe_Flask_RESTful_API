from flask import jsonify, request, Blueprint
from flask_jwt_extended import jwt_required, verify_jwt_in_request
from marshmallow import Schema, fields
from sqlalchemy import text
from ..conn import Session

delete_module_bp = Blueprint('delete_module', __name__)

class DeleteModuleSchema(Schema):
    module_id = fields.Int(required=True)

@delete_module_bp.route('/delete_module', methods=['DELETE'])
@jwt_required()
def delete_module():
    token = verify_jwt_in_request()
    if not token['fresh']:
        return jsonify({'error': 'Expired token'})
    
    data = request.get_json()
    schema = DeleteModuleSchema()
    errors = schema.validate(data)

    if errors:
        return jsonify({'errors': errors}), 400
    
    session = Session()
    
    try:
        session.execute(
            text("DELETE FROM modules WHERE module_id = :id"),
            {'id': data['module_id']},
        )
        session.commit()
        return jsonify({'success': True}), 200
    except Exception as e:
        session.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        session.close()