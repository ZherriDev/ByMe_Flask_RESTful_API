from flask import jsonify, request, Blueprint, render_template
from flask_jwt_extended import jwt_required, verify_jwt_in_request, decode_token
from flask_mailman import EmailMultiAlternatives
from cryptography.fernet import Fernet
from urllib.parse import quote, unquote
from marshmallow import Schema, fields
from sqlalchemy import text
import bcrypt
import hashlib
from ..conn import Session

change_email_bp = Blueprint('change_email', __name__)

class ChangeEmail(Schema):
    doctor_id = fields.Int(required=True)
    old_email = fields.Str(required=True)
    new_email = fields.Str(required=True)

@change_email_bp.route('/change_email', methods=['POST'])
@jwt_required()
def change_email():
    data = request.get_json()
    schema = ChangeEmail()
    errors = schema.validate(data)
    
    if errors:
        return jsonify({'errors': errors}), 400
    
    session = Session()
    
    try:
        result = session.execute(
            text('SELECT email, name FROM doctors WHERE doctor_id = :doctor_id'),
            {'doctor_id': data['doctor_id']}
        ).fetchone()
        
        if result and result[0] == data['old_email']:
            name = result[1]
            email_key = hashlib.md5(data['new_email'].encode('utf8')).hexdigest()
            
            session.execute(
                text('UPDATE doctors SET key_email = :key_email WHERE doctor_id = :doctor_id'),
                {
                    'key_email': email_key, 
                    'doctor_id': data['doctor_id']
                }
            )
            session.commit()
        
            subject, from_email, to = 'ByMe Information Technology - Email Confirmation', 'cinesquadd@gmail.com', data['new_email']
            text_content = f'Hi {name},\nYour new email is almost registered in our application, we just need you to confirm your new email.\n\
                Please confirm your new email by clicking the link below:\nhttps://api-py-byme.onrender.com/auth/confirm_new_email/{email_key}'
            html_content = render_template("confirm_new_email.html", name=name, email_hash=email_key)
            msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
    except Exception as e:
        session.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        session.close()