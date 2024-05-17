from flask import jsonify, request, Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity, verify_jwt_in_request
from marshmallow import Schema, fields
from sqlalchemy import text
from ..conn import Session
from ..logger import logger


select_sessions_bp = Blueprint('select_sessions', __name__)

class GetSessionsSchema(Schema):
    doctor_id = fields.Int(required=True)

@select_sessions_bp.route('/select_sessions/<int:id>', methods=['GET'])
@jwt_required()
def select_sessions(id):

    doctor_id = get_jwt_identity()
    
    data = {'doctor_id': id}
    schema = GetSessionsSchema()
    errors = schema.validate(data)
    
    jwt_data = verify_jwt_in_request()
    jti = jwt_data[1]['jti'];

    if errors:
        logger.error(f"Invalid sessions select request made by Doctor ID:{doctor_id}.", extra={"method": "GET", "statuscode": 400})
        return jsonify({'errors': errors}), 400
    
    session = Session()


    try:
        sessions = []
        result = session.execute(
            text('SELECT * FROM sessions WHERE doctor_id = :doctor_id'),
            {'doctor_id': doctor_id}
        ).fetchall()

        result_id = session.execute(text('SELECT session_id FROM sessions WHERE jti = :jti'),
            {
                "jti": jti
            }).fetchone()
        
        if result_id:
            session_id = result_id[0]
        
        for sessionUser in result:
            sessionUser = sessionUser._asdict()
            sessions.append(sessionUser)
        
        logger.info(f"Doctor ID:{doctor_id} selected Sessions", extra={"method": "GET", "statuscode": 200})
        return jsonify({'success': True, 'sessions': sessions, 'current_session': session_id}), 200
    except Exception as e:
        session.rollback()
        logger.error(f"Doctor ID:{doctor_id}'s attempt to select Sessions failed.", extra={"method": "GET", "statuscode": 500, "exc": str(e)})
        return jsonify({'error': str(e)}), 500
    finally:
        session.close()
