from flask import jsonify, request, Blueprint
from flask_jwt_extended import create_access_token, decode_token
from marshmallow import Schema, fields
from datetime import datetime
from sqlalchemy import text
import bcrypt
import socket
import requests
from ..conn import Session

login_bp = Blueprint('login', __name__)

class LoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True)

@login_bp.route('/login', methods = ['POST'])
def login_user():
    data = request.get_json()
    schema = LoginSchema()
    errors = schema.validate(data)
    
    if errors:
        return jsonify({'errors': errors}), 400
    
    session = Session()
    
    try:
        result = session.execute(
            text("SELECT * FROM doctors WHERE email = :email"),
            {'email': data['email']},
        ).fetchone()
        
        if result:
            result = result._asdict()
            if bcrypt.checkpw(data['password'].encode('utf8'), result['password'].encode('utf8')):
                if result['email_ver'] == 1:
                    user_claims = {'email': result['email'],}
                    token = create_access_token(identity=result['doctor_id'], additional_claims=user_claims, expires_delta=False)
                    
                    decoded_token = decode_token(token)
                    
                    jti = decoded_token['jti']

                    def get_public_ip():

                        try:
                            response = requests.get('https://api.ipify.org')
                            if response.status_code == 200:
                                return response.text
                            else:
                                return None
                        except Exception as e:
                            print("Erro ao obter o IP público:", e)
                            return None

                    public_ip = get_public_ip()
                    if public_ip:
                        print("Seu endereço IP público é:", public_ip)
                    else:
                        print("Não foi possível obter o endereço IP público.")


                    

                    session.execute(
                        text("INSERT INTO sessions (doctor_id, date_time, jti) VALUES (:doctor_id, :date_time, :jti)"),
                        {
                            'doctor_id': result['doctor_id'],
                            'date_time': datetime.now(),
                            'jti': jti,
        
                        }
                    )
                    session.commit()
                    return jsonify({'success': True, 'token': token}), 200
                else:
                    return jsonify({'error': 'Email is not yet verified'}), 401
            else:
                return jsonify({'error': 'Invalid Credentials'}), 401
        else:
            return jsonify({'error': 'Invalid Credentials'}), 401
    except Exception as e:
        session.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        session.close()