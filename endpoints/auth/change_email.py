from flask import jsonify, request, Blueprint, render_template
from flask_jwt_extended import jwt_required, verify_jwt_in_request, decode_token
from flask_mailman import EmailMultiAlternatives
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
            text('SELECT email, fullname FROM doctors WHERE doctor_id = :doctor_id'),
            {'doctor_id': data['doctor_id']}
        ).fetchone()
        
        if result and result[0] == data['old_email']:
            name = result[1]
            old_email = data['old_email']
            new_email = data['new_email']
            email_key = hashlib.md5(new_email.encode('utf8')).hexdigest()
            
            session.execute(
                text('UPDATE doctors SET email = :email, key_email = :key_email, email_ver = 0 WHERE doctor_id = :doctor_id'),
                {
                    'email': new_email,
                    'key_email': email_key, 
                    'doctor_id': data['doctor_id']
                }
            )
            session.commit()
            
            subject, from_email, to = 'ByMe Information Technology - Email Change Notification', 'cinesquadd@gmail.com', old_email
            text_content = f'Hi {name},\nThere has been a change to your account email on our application.\n\
                The same went from {old_email} to {new_email}.\n\
                If you were not the one who changed your account email, please contact us about what happened: byme@support.com'
            html_content = render_template("notification_email_change.html", name=name, old_email=old_email, new_email=new_email)
            msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
        
            subject, from_email, to = 'ByMe Information Technology - Email Confirmation', 'cinesquadd@gmail.com', new_email
            text_content = f'Hi {name},\nYour new email is almost registered on our application, we just need you to confirm your new email.\n\
                Please confirm your new email by clicking the link below:\nhttps://api-py-byme.onrender.com/auth/confirm_email/{email_key}'
            html_content = render_template("confirm_new_email.html", name=name, email_hash=email_key)
            msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            
            return jsonify({'success': True}), 200
        else:
            return jsonify({'error': 'Invalid email address'})
    except Exception as e:
        session.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        session.close()