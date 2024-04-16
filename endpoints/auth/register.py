from flask import jsonify, request, Blueprint, render_template
from flask_mailman import EmailMultiAlternatives
from marshmallow import Schema, fields
from sqlalchemy import text
import bcrypt
import hashlib
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
        
        name = data['name']
        email_key = hashlib.md5(data['email'].encode('utf8')).hexdigest()
        
        session.execute(
            text("INSERT INTO doctors (fullname, speciality, email, password, key_email) VALUES (:fullname, :speciality, :email, :senha, :key)"),
            {
                'fullname': name,
                'speciality': data['speciality'],
                'email': data['email'],
                'senha': hash_password,
                'key': email_key
            },
        )
        session.commit()
        
        subject, from_email, to = 'ByMe Information Technology - Email Confirmation', 'cinesquadd@gmail.com', data['email']
        text_content = f'Hi {name},\nYour registration is almost complete on our application, we just need you to confirm your email.\n\
            Please confirm your email by clicking the link below:\nhttps://api-py-byme.onrender.com/auth/confirm_email/{email_key}'
        html_content = render_template("confirm_email.html", name=name, email_hash=email_key)
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        
        return jsonify({'success': True}), 201
    except Exception as e:
        session.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        session.close()