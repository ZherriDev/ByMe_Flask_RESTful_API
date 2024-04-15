from flask import jsonify, request, Blueprint, render_template
from flask_mailman import EmailMultiAlternatives
from marshmallow import Schema, fields
from sqlalchemy import text
import bcrypt
from ..conn import Session

change_password_bp = Blueprint('change_password', __name__)

class ChangePasswordSchema(Schema):
    old_password = fields.Str(required=True)
    new_password = fields.Str(required=True)
    confirm_password = fields.Str(required=True)


@change_password_bp.route('/change_password', methods = ['POST'])
def change_password():
    data = request.get_json()
    schema = ChangePasswordSchema()
    errors = schema.validate(data)

    if errors:
        return jsonify(errors), 400
    
    session = Session()

    try:
        result = session.execute(
            text(''),
            {'email': data['email']}
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    finally:
        session.close()
    
