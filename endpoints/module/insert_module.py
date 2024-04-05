from flask import jsonify, request, Blueprint
from marshmallow import Schema, fields
from datetime import datetime
from sqlalchemy import text
from ..conn import Session

insert_module_bp = Blueprint('insert_module', __name__)

class InsertModuleSchema(Schema):
    patient_id = fields.Int(required=True)
    episode = fields.String(required=True)
    module = fields.String(required=True)
    status = fields.String(required=True)

@insert_module_bp.route('/insert_module', methods=['POST'])
def insert_module():
    data = request.get_json()
    schema = InsertModuleSchema()
    errors = schema.validate(data)
    
    if errors:
        return jsonify({'errors': errors, 'data': data}), 400
    
    session = Session()
    try:
        session.execute(
            text("INSERT INTO modules (patient_id, episode, module, status) VALUES (:patient_id, :episode , :module, :status)"),
            {
                'patient_id': data['patient_id'], 
                'episode': data['episode'],
                'module': data['module'],
                'status': data['status']
            },
            
        )
        session.commit()
        return jsonify({'success': True}), 201
    except Exception as e:
        session.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        session.close()