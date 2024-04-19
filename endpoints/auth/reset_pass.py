from flask import jsonify, request, Blueprint, render_template
from flask_mailman import EmailMultiAlternatives
from marshmallow import Schema, fields
from sqlalchemy import text
import bcrypt
import hashlib
from ..conn import Session
from ..logger import logger

reset_pass_bp = Blueprint('reset_pass', __name__)

class ResetPasswSchema(Schema):
    key = fields.Str(required=True)

@reset_pass_bp.route('/reset_pass/<key>', methods=['GET'])
def request_reset_pass(key):
    data = {'key': key}
    schema = ResetPasswSchema()
    errors = schema.validate(data)

    if errors:
        logger.error(f"Invalid password reset request made", extra={"method": "GET", "statuscode": 400})
        return jsonify(errors), 400
    
    session = Session()

    try:
        result = session.execute(
            text("SELECT * FROM doctors WHERE key_pass = :key"),
            {
                'key': data['key'],
            },
        ).fetchone()

        if result:
            result = result._asdict()
            id = result['doctor_id']
            
            logger.info(f"Doctor ID:{id} key confirmed.", extra={"method": "GET", "statuscode": 200})
            return render_template('reset_pass_form.html', id=id, key=data['key'])
        else:
            logger.warning(f"Invalid password key request made", extra={"method": "GET", "statuscode": 400})
            return jsonify({'errors': 'Invalid key'}), 400
        
    except Exception as e:
        session.rollback()
        logger.error(f"A password reset request failed.", extra={"method": "GET", "statuscode": 500, "exc": str(e)})
        return jsonify({'errors': str(e)}), 500
    finally:
        session.close()