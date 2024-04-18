from flask import jsonify, request, Blueprint
from flask_jwt_extended import jwt_required, verify_jwt_in_request, get_jwt_identity
from marshmallow import Schema, fields
from sqlalchemy import text
from ..conn import Session
from ..logger import logger


select_module_bp = Blueprint('select_module', __name__)

class ShowModuleSchema(Schema):
    patient_id = fields.Int(required=True)

@select_module_bp.route('/select_module/<int:id>', methods=['GET'])
@jwt_required()
def select_modules(id):

    doctor_id = get_jwt_identity()
    
    data = jsonify({'patient_id': id})
    schema = ShowModuleSchema()
    errors = schema.validate(data)

    if errors:
        logger.error(f"Invalid request made by Doctor ID: {doctor_id}", extra={"method": "GET", "statuscode": 400})
        return jsonify({'errors': errors}), 400
    
    session = Session()
    patient_id = data['patient_id']
    
    try:
        modules = []
        result = session.execute(
            text('SELECT * FROM modules WHERE patient_id = :patient_id'),
            {'patient_id': patient_id}
        ).fetchall()
        
        for module in result:
            module = module._asdict()
            modules.append(module)
        
        logger.info(f"Doctor ID: {doctor_id} selected all modules from Patiend ID: {patient_id}", extra={"method": "GET", "statuscode": 200})
        return jsonify({'success': True, 'modules': modules}), 200
    except Exception as e:
        session.rollback()
        logger.warning(str(e), extra={"methos": "GET", "statuscode": 500})
        return jsonify({'error': str(e)}), 500
    finally:
        session.close()