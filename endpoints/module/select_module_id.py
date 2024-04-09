from flask import jsonify, request, Blueprint
from flask_jwt_extended import jwt_required, verify_jwt_in_request
from marshmallow import Schema, fields
from sqlalchemy import text
from ..conn import Session

select_module_id_bp = Blueprint('select_module_id', __name__)

class SelectModuleIDSchema(Schema):
    module_id = fields.Int(required=True)

@select_module_id_bp.route('/select_module/<int:id>', methods=['GET'])
@jwt_required()
def select_module_id(id):
    token = verify_jwt_in_request()
    if not token['fresh']:
        return jsonify({'error': 'Expired token'})
    
    data = jsonify({'module_id': id})
    schema = SelectModuleIDSchema()
    errors = schema.validate(data)

    if errors:
        return jsonify({'errors': errors}), 400
    
    session = Session()
    
    try:
        result = session.execute(
            text('SELECT * FROM modules WHERE module_id = :module_id'),
            {'module_id': data['module_id']}
        ).fetchone()
        if result:
            result = result._asdict()
        return jsonify({'success': True, 'module': result}), 200
    except Exception as e:
        session.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        session.close()