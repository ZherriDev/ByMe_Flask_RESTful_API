from flask import jsonify, request, Blueprint
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
                return jsonify({'success': True, 'user': result}), 200
            else:
                return jsonify({'error': 'Palavra-passe incorreta'}), 400
        else:
            return jsonify({'error': 'Utilizador não encontrado'}), 400
    except Exception as e:
        session.rollback()
        return jsonify({'error': str(e)}), 500