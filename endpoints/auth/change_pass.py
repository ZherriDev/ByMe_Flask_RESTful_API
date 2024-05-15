from flask import jsonify, request, Blueprint, render_template
from flask_mailman import EmailMultiAlternatives
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import Schema, fields
from sqlalchemy import text
import bcrypt
from ..conn import Session
from ..logger import logger
from ..utils import limiter

change_password_bp = Blueprint('change_password', __name__)

class ChangePasswordSchema(Schema):
    doctor_id = fields.Int(required=True)
    old_password = fields.Str(required=True)
    new_password = fields.Str(required=True)


@change_password_bp.route('/change_password', methods = ['POST'])
@jwt_required()
@limiter.limit("5 per minute")
def change_password():
    data = request.get_json()
    schema = ChangePasswordSchema()
    errors = schema.validate(data)
    doctor_id = get_jwt_identity()

    if errors:
        logger.error(f"Invalid request made by Doctor ID:{doctor_id}.", extra={"method": "POST", "statuscode": 400})
        return jsonify(errors), 400
        
    session = Session()

    try:
        result_old_pass = session.execute(text('SELECT * FROM doctors WHERE doctor_id = :doctor_id'),
            {
                'doctor_id': data['doctor_id'],
            },
        ).fetchone()
        
        result = result_old_pass._asdict()
        name = result['fullname']

        if bcrypt.checkpw(data['old_password'].encode('utf8'), result['password'].encode('utf8')):
            salt = bcrypt.gensalt()
            hash_password = bcrypt.hashpw(data['new_password'].encode('utf8'), salt)
            session.execute(
                text('UPDATE doctors SET password = :password WHERE doctor_id = :doctor_id'),
                {
                    'doctor_id': data['doctor_id'],
                    'password': hash_password,
                },
            )
            session.commit()
        
            
            session.execute(text('UPDATE sessions SET in_blacklist = 1 WHERE doctor_id = :doctor_id'),
                {
                    'doctor_id': data['doctor_id'],
                },
            )

            session.commit()

            subject, from_email, to = 'ByMe Information Technology - Password Change Notification', 'cinesquadd@gmail.com', result['email']
            text_content = f'Hi {name},\nThere has been a change to your account password on our application.\n\
                If you were not the one who changed your account password, please contact us about what happened: byme@support.com'
            html_content = render_template("notification_pass_change.html", name=name)
            msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
            msg.attach_alternative(html_content, "text/html")
            msg.send()

            logger.info(f"Doctor ID:{doctor_id} changed his password.", extra={"method": "POST", "statuscode": 200})
            return jsonify({'success': True}), 200    
        else:
            logger.warning(f"Doctor ID:{doctor_id} tried to change his password but the old_password was invalid.", extra={"method": "POST", "statuscode": 200})
            return jsonify({'message': 'Invalid old password'}), 400
        
    except Exception as e:
        session.rollback()
        logger.error(f"Doctor ID:{doctor_id}'s attempt to change his password failed.", extra={"method": "POST", "statuscode": 500, "exc": str(e)})
        return jsonify({'error': str(e)}), 500
    finally:
        session.close()
    
