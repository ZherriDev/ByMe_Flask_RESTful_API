from flask import jsonify, request, Blueprint, render_template
from flask_mailman import EmailMultiAlternatives
from marshmallow import Schema, fields
from sqlalchemy import text
import bcrypt
import hashlib
from ..conn import Session

reset_pass_form_bp = Blueprint('reset_pass_form', __name__)

class ResetPassFormSchema(Schema):
    doctor_id = fields.Int(required=True)
    password = fields.Str(required=True)
    key = fields.Str(required=True)

@reset_pass_form_bp.route('/reset_pass_form', methods=['POST'])
def reset_pass_form():
    data = request.get_json()
    schema = ResetPassFormSchema()
    errors = schema.validate(data)

    if errors:
        return jsonify(errors), 400
    
    session = Session()

    salt = bcrypt.gensalt()
    hash_password = bcrypt.hashpw(data['password'].encode('utf8'), salt)

    try:   
        result = session.execute(text("SELECT * FROM doctors WHERE key_pass = :key_pass"),
            {
                'key_pass': data['key'],
            }
        ).fetchone()

        if result:
            session.execute(text("UPDATE doctors SET key_pass = NULL, password = :password WHERE doctor_id = :doctor_id"),
                {
                    'password': hash_password,
                    'doctor_id': data['doctor_id'],
                }
            )
            session.commit()
            return jsonify({'message': 'Password reset successfully'}), 200
        else:
            return jsonify({'message': 'Invalid key'}), 400
    except Exception as e:
        session.rollback()
        return jsonify({'message': str(e)}), 500
    finally:
        session.close()