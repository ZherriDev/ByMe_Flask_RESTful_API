from flask import jsonify, request, Blueprint
from flask_jwt_extended import jwt_required
from marshmallow import Schema, fields
from sqlalchemy import text
from ..conn import Session
from ..logger import logger

delete_doctor_bp = Blueprint('delete_doctor', __name__)

class DeleteDoctorSchema(Schema):
    doctor_id = fields.Int(required=True)

@delete_doctor_bp.route('/delete_doctor', methods=['DELETE'])
@jwt_required()
def delete_doctor():
    
    data = request.get_json()
    schema = DeleteDoctorSchema()
    errors = schema.validate(data)

    if errors:
        logger.error(f"Invalid delete doctor request made", extra={"method": "DELETE", "statuscode": 400})
        return jsonify({'errors': errors}), 400
    
    session = Session()
    
    try:
        result = session.execute(
            text("SELECT patient_id FROM patients WHERE doctor_id = :id"),
            {'id': data['doctor_id']},
        ).fetchall()
        
        if result:
            for patient_id in result:
                session.execute(
                    text("DELETE FROM modules WHERE patient_id = :patient_id"),
                    {'patient_id': patient_id}
                )
                session.commit()
            
            session.execute(
                text("DELETE FROM patients WHERE doctor_id = :id"),
                {'id': data['doctor_id']},
            )
            session.commit()
            
        else:
            session.execute(
                text("DELETE FROM doctors WHERE doctor_id = :id"),
                {'id': data['doctor_id']},
            )
            session.commit()
        
        logger.info(f"Deletion of Doctor ID:{data['doctor_id']} done successfully.", extra={"method": "DELETE", "statuscode": 200})
        return jsonify({'success': True}), 200
    except Exception as e:
        session.rollback()
        logger.error(f"An attempt to delete Doctor ID:{data['doctor_id']} failed.", extra={"method": "DELETE", "statuscode": 500, "exc": str(e)})
        return jsonify({'error': str(e)}), 500
    finally:
        session.close()