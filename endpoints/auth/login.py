from flask import jsonify, request, Blueprint
from flask_jwt_extended import create_access_token, decode_token
from marshmallow import Schema, fields
from datetime import datetime
from sqlalchemy import text
import bcrypt
from ..conn import Session
from ..logger import logger
from ..utils import limiter


login_bp = Blueprint('login', __name__)

class LoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True)
    ip_address = fields.Str(required=False)
    device = fields.Str(required=False)
    operational_system = fields.Str(required=False)
    location = fields.Str(required=False)

@login_bp.route('/login', methods = ['POST'])
@limiter.limit("15 per minute")
def login_user():
    data = request.get_json()
    schema = LoginSchema()
    errors = schema.validate(data)
    
    if errors:
        logger.error(f"Invalid login request made", extra={"method": "POST", "statuscode": 400})
        return jsonify({'errors': errors}), 400
    
    session = Session()
    
    try:
        result = session.execute(
            text("SELECT * FROM doctors WHERE email = :email"),
            {'email': data['email']},
        ).fetchone()
        
        if not result:
            logger.warning(f"Doctor with email '{data['email']}' not found.", extra={"method": "POST", "statuscode": 401})
            return jsonify({'error': 'Invalid Credentials'}), 401
            
        result = result._asdict()
        if bcrypt.checkpw(data['password'].encode('utf8'), result['password'].encode('utf8')):
            if result['email_ver'] == 1:
                user_claims = {'email': result['email'],}
                if result['admin'] == 1:
                    user_claims['admin'] = 1
                token = create_access_token(identity=result['doctor_id'], additional_claims=user_claims, expires_delta=False)
                
                decoded_token = decode_token(token)
                
                jti = decoded_token['jti']

                session.execute(
                    text("INSERT INTO sessions (doctor_id, date_time, ip_address, device, operational_system, location, jti) \
                        VALUES (:doctor_id, :date_time, :ip_address, :device, :operational_system, :location, :jti)"),
                    {
                        'doctor_id': result['doctor_id'],
                        'date_time': datetime.now(),
                        'ip_address': data['ip_address'],
                        'device': data['device'],
                        'operational_system': data['operational_system'],
                        'location': data['location'],
                        'jti': jti,
                    }
                )
                session.commit()
                
                logger.info(f"Doctor ID:{result['doctor_id']} logged in.", extra={"method": "POST", "statuscode": 200})
                return jsonify({'success': True, 'token': token, 'doctor_id': result['doctor_id']}), 200
            else:
                logger.warning(f"Doctor ID:{result['doctor_id']}'s login attempt was denied. Email not confirmed.", extra={"method": "POST", "statuscode": 403})
                return jsonify({'error': 'Email is not yet verified'}), 403
        else:
            logger.warning(f"Doctor ID:{result['doctor_id']} entered the incorrect password.", extra={"method": "POST", "statuscode": 401})
            return jsonify({'error': 'Invalid Credentials'}), 401
        
    except Exception as e:
        session.rollback()
        logger.error(f"A login attempt failed.", extra={"method": "POST", "statuscode": 500, "exc": str(e)})
        return jsonify({'error': str(e)}), 500
    finally:
        session.close()
