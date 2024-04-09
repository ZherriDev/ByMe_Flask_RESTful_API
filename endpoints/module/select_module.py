from flask import jsonify, request, Blueprint
from flask_jwt_extended import jwt_required, verify_jwt_in_request
from marshmallow import Schema, fields
from sqlalchemy import text
from ..conn import Session

select_module_bp = Blueprint('select_module', __name__)

class ShowModuleSchema(Schema):
    patient_id = fields.Int(required=True)

@select_module_bp.route('/select_module/<int:id>', methods=['GET'])
@jwt_required()
def select_modules(id):
    token = verify_jwt_in_request()
    if not token['fresh']:
        return jsonify({'error': 'Expired token'})
    
    data = jsonify({'patient_id': id})
    schema = ShowModuleSchema()
    errors = schema.validate(data)

    if errors:
        return jsonify({'errors': errors}), 400
    
    session = Session()
    
    try:
        modules = []
        result = session.execute(
            text('SELECT * FROM modules WHERE patient_id = :patient_id'),
            {'patient_id': data['patient_id']}
        ).fetchall()
        
        for module in result:
            module = module._asdict()
            modules.append(module)
        
        return jsonify({'success': True, 'modules': modules}), 200
    except Exception as e:
        session.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        session.close()