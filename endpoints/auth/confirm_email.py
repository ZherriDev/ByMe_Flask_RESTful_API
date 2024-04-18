from flask import jsonify, request, Blueprint, render_template
from flask_mailman import EmailMultiAlternatives
from marshmallow import Schema, fields
from sqlalchemy import text
import bcrypt
from ..conn import Session
from ..logger import logger

confirm_email_bp = Blueprint('confirm_email', __name__)

class ConfirmEmailSchema(Schema):
    key = fields.Str(required=True)

@confirm_email_bp.route('/confirm_email/<key>', methods=['GET'])
def confirm_email(key):
    data = {'key': key}
    schema = ConfirmEmailSchema()
    errors = schema.validate(data)
    
    if errors:
        logger.error(f"Invalid request made", extra={"method": "GET", "statuscode": 400})
        return jsonify({'errors': errors}), 400
    
    session = Session()
    
    try:
        msg = 'success'
        result = session.execute(
            text('SELECT * FROM doctors WHERE key_email = :key'),
            {'key': key}
        ).fetchone()

        if not result:
            msg = 'invalid key'
            logger.warning(f"Invalid email key request made.", extra={"method": "GET", "statuscode": 401})
        else:
            result = result._asdict()
            session.execute(
                text('UPDATE doctors SET key_email = NULL, email_ver = 1 WHERE key_email = :key'),
                {'key': key}
            )
            session.commit()
            logger.info(f"The email {result['email']} has been confirmed.", extra={"method": "GET", "statuscode": 200})
        
        return render_template('success.html', msg=msg)
    except Exception as e:
        session.rollback()
        logger.error(f"An email confirmation attempt failed.", extra={"method": "GET", "statuscode": 500, "exc": str(e)})
        return jsonify({'error': str(e)}), 500
    finally:
        session.close()