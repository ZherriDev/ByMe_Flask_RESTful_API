from flask import jsonify, request, Blueprint
from flask_jwt_extended import jwt_required
from marshmallow import Schema, fields
from sqlalchemy import text
from ..conn import Session

select_module_bp = Blueprint('select_module_bp', __name__)

class ShowModuleSchema(Schema):
    patient_id = fields.Int(required=True)

@select_module_bp.route('/select_modules', methods=['POST'])
@jwt_required()
def select_modules():
    data = request.get_json()
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