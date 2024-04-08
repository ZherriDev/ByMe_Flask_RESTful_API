from flask import jsonify, request, Blueprint
from flask_jwt_extended import create_access_token
from marshmallow import Schema, fields
from sqlalchemy import text
import bcrypt
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
                user_claims = {'email': result['email'],}
                token = create_access_token(identity=result['doctor_id'], additional_claims=user_claims)
                return jsonify({'success': True, 'token': token}), 200
            else:
                return jsonify({'error': 'Invalid Credentials'}), 401
        else:
            return jsonify({'error': 'Invalid Credentials'}), 401
    except Exception as e:
        session.rollback()
        return jsonify({'error': str(e)}), 500