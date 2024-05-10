from flask import jsonify, request, Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import Schema, fields
from sqlalchemy import text
from ..conn import Session
from ..logger import logger

select_patient_bp = Blueprint('select_patient', __name__)

class SelectPatientSchema(Schema):
    doctor_id = fields.Int(required=True)
    search = fields.Str(allow_none=True)
    order = fields.Str(allow_none=True)
    state = fields.Str(allow_none=True)

@select_patient_bp.route('/select_patient/<int:id>/', defaults={'search': None, 'order': None, 'state': None})
@select_patient_bp.route('/select_patient/<int:id>/<search>/<order>/<state>', methods=['GET'])
@jwt_required()
def select_patient(id, search, order, state):

    data = {'doctor_id': id, 'search': search, 'order': order, 'state': state}
    schema = SelectPatientSchema()
    errors = schema.validate(data)

    if errors:
        logger.error(f"Invalid patient select request made by Doctor ID:{data['doctor_id']}.", extra={"method": "GET", "statuscode": 400})
        return jsonify({'errors': errors}), 400
        
    session = Session()
    
    try:
        text_state = ""
        text_order = ""
        
        if order:
            if order == 'a-z':
                text_order = " ORDER BY name ASC"
            elif order == 'recent':
                text_order = " ORDER BY admission_date DESC"
        
        if state:
            if state == 'In Treatment':
                text_state = " AND status = 'In Treatment'"
            elif state == 'Awaiting Treatment':
                text_state = " AND status = 'Awaiting Treatment'"
            elif state == 'Completed Treatment':
                text_state = " AND status = 'Completed Treatment'"

        patients = []

        if search:
            sql = "SELECT * FROM patients WHERE doctor_id = :doctor_id AND name LIKE :search{}{}"
            result = session.execute(
                text(sql.format(text_state, text_order)),
                {
                    'doctor_id': data['doctor_id'],
                    'search': "%" + data['search'] + "%"
                }
            ).fetchall()
        else:
            sql = "SELECT * FROM patients WHERE doctor_id = :doctor_id{}{}"
            result = session.execute(
                text(sql.format(text_state, text_order)),
                {'doctor_id': data['doctor_id']}
            ).fetchall()
        
        for patient in result:
            patient = patient._asdict()
            patients.append(patient)
        
        logger.info(f"Doctor ID:{data['doctor_id']} selected Patients.", extra={"method": "GET", "statuscode": 200})
        return jsonify({'success': True, 'patients': patients}), 200
    except Exception as e:
        session.rollback()
        logger.error(f"Doctor ID:{data['doctor_id']}'s attempt to select Patients failed.", extra={"method": "GET", "statuscode": 500, "exc": str(e)})
        return jsonify({'error': str(e)}), 500
    finally:
        session.close()
