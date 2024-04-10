from flask import jsonify, request, Blueprint, render_template
from flask_mailman import EmailMultiAlternatives
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
        
        subject, from_email, to = 'ByMe Information Technology - Email Confirmation', 'cinesquadd@gmail.com', 'lucas18627@gmail.com'
        text_content = 'Teste'
        name = data['name']
        html_content = render_template("confirm_email.html", name=name)
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        
        return jsonify({'success': True}), 201
    except Exception as e:
        session.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        session.close()