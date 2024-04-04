from flask import jsonify, request, Blueprint
from marshmallow import Schema, fields
from sqlalchemy import text
import bcrypt
from ..conn import Session

register_bp = Blueprint('register', __name__)

class RegisterSchema(Schema):
    name = fields.Str(required=True)
    speciality = fields.Str(required=True)
    email = fields.Email(required=True)
    password = fields.Str(required=True)

@register_bp.route('/register', methods = ['POST'])
def register_user():
    data = request.get_json()
    schema = RegisterSchema()
    errors = schema.validate(data)
    
    if errors:
        return jsonify({'errors': errors}), 400
    
    session = Session()
    
    try:
        salt = bcrypt.gensalt()
        hash_password = bcrypt.hashpw(data['password'].encode('utf8'), salt)
        session.execute(
            text("INSERT INTO doctors (fullname, speciality, email, password) VALUES (:fullname, :speciality, :email, :senha)"),
            {
                'fullname': data['name'],
                'speciality': data['speciality'],
                'email': data['email'],
                'senha': hash_password
            },
        )
        session.commit()
        return jsonify({'success': True}), 201
    except Exception as e:
        session.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        session.close()