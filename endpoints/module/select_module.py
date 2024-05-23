from flask import jsonify, request, Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import Schema, fields
from sqlalchemy import text
from ..conn import Session
from ..logger import logger


select_module_bp = Blueprint('select_modules', __name__)

class ShowModulesSchema(Schema):
    patient_id = fields.Int(required=True)

@select_module_bp.route('/select_modules/<int:id>', methods=['GET'])
@jwt_required()
def select_modules(id):

    doctor_id = get_jwt_identity()
    
    data = {'patient_id': id}
    schema = ShowModulesSchema()
    errors = schema.validate(data)

    if errors:
        logger.error(f"Invalid modules select request made by Doctor ID:{doctor_id}.", extra={"method": "GET", "statuscode": 400})
        return jsonify({'errors': errors}), 400
    
    session = Session()
    patient_id = data['patient_id']
    
    try:
        modules = []
        result = session.execute(
            text('SELECT * FROM modules WHERE patient_id = :patient_id ORDER BY creation_date DESC'),
            {'patient_id': patient_id}
        ).fetchall()
        
        for module in result:
            module = module._asdict()
            modules.append(module)
        
        logger.info(f"Doctor ID:{doctor_id} selected all modules from Patient ID:{patient_id}.", extra={"method": "GET", "statuscode": 200})
        return jsonify({'success': True, 'modules': modules}), 200
    except Exception as e:
        session.rollback()
        logger.error(f"Doctor ID:{doctor_id}'s attempt to select Modules from Patient ID:{patient_id} failed.", extra={"method": "GET", "statuscode": 500, "exc": str(e)})
        return jsonify({'error': str(e)}), 500
    finally:
        session.close()
