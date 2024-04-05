from flask import jsonify, request, Blueprint
from marshmallow import Schema, fields
from sqlalchemy import text
from ..conn import Session

select_patient_bp = Blueprint('select_patient_bp', __name__)

class ShowPatientSchema(Schema):
    doctor_id = fields.Int(required=True)
    order = fields.Str(required=False)
    state = fields.Str(required=False)

@select_patient_bp.route('/show_patients', methods=['POST'])
def show_patients():

    data = request.get_json()
    schema = ShowPatientSchema()
    errors = schema.validate(data)

    if errors:
        return jsonify({'errors': errors}), 400
        
    session = Session()
    
    order = data.get('order', None)
    state = data.get('state', None)
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
        sql = "SELECT * FROM patients WHERE doctor_id = :doctor_id{}{}"
        
        result = session.execute(
            text(sql.format(text_state, text_order)),
            {'doctor_id': data['doctor_id']}
        ).fetchall()
        
        for patient in result:
            patient = patient._asdict()
            patients.append(patient)
        
        return jsonify({'success': True, 'patients': patients}), 200
    except Exception as e:
        session.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        session.close()