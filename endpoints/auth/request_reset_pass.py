from flask import jsonify, request, Blueprint, render_template
from flask_mailman import EmailMultiAlternatives
from marshmallow import Schema, fields
from sqlalchemy import text
import bcrypt
import hashlib
from ..conn import Session
from ..logger import logger
from ..utils import limiter

request_reset_pass_bp = Blueprint('request_reset_pass', __name__)

class RequestResetPassSchema(Schema):
    email = fields.Str(required=True)

@request_reset_pass_bp.route('/request_reset_pass', methods=['POST'])
@limiter.limit("10 per minute")
def request_reset_pass():
    data = request.get_json()
    schema = RequestResetPassSchema()
    errors = schema.validate(data)
    
    if errors:
        logger.error(f"Invalid password reset request made", extra={"method": "POST", "statuscode": 400})
        return jsonify({'errors': errors}), 400
    
    session = Session()
    
    try:
        result = session.execute(
            text('SELECT * FROM doctors WHERE email = :email'),
            {'email': data['email']}
        ).fetchone()
        
        if result:
            result = result._asdict()
            id = result['doctor_id']
            name = result['fullname']
            pass_key = hashlib.md5(data['email'].encode('utf8')).hexdigest()
            
            subject, from_email, to = 'ByMe Information Technology - Reset Password', 'cinesquadd@gmail.com', data['email']
            text_content = f'Hi {name},\nYou have made a password reset request on our application.\n\
                Click here to reset yout password:\nhttps://api-py-byme.onrender.com/auth/reset_pass/{pass_key}'
            html_content = render_template("reset_pass.html", name=name, pass_hash=pass_key)
            msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
            msg.attach_alternative(html_content, "text/html")
            msg.send()

            session.execute(
                text('UPDATE doctors SET key_pass = :key_pass WHERE doctor_id = :id'),
                {
                    'key_pass': pass_key,
                    'id': id
                }
            )
            session.commit()
            
            logger.info(f"Doctor ID:{id} made a request to reset password.", extra={"method": "POST", "statuscode": 200})
            return jsonify({'success': True, 'message': 'Email sent'}), 200
        else:
            logger.warning(f"Email not found in a password reset request.", extra={"method": "POST", "statuscode": 400})
            return jsonify({'errors': 'Email not found'}), 400
        
    except Exception as e:
        session.rollback()
        logger.error(f"A password reset attempt failed.", extra={"method": "POST", "statuscode": 500, "exc": str(e)})
        return jsonify({'errors': str(e)}), 500
    finally:
        session.close()