from flask import jsonify, request, Blueprint, render_template
from flask_mailman import EmailMultiAlternatives
from marshmallow import Schema, fields
from sqlalchemy import text
import bcrypt
import hashlib
from ..conn import Session

reset_pass_bp = Blueprint('reset_pass', __name__)

class ResetPasswSchema(Schema):
    key = fields.Str(required=True)

@reset_pass_bp.route('/reset_pass/<key>', methods=['GET'])
def request_reset_pass(key):
    data = {'key': key}
    schema = ResetPasswSchema()
    errors = schema.validate(data)

    if errors:
        return jsonify(errors), 400
    
    session = Session()

    try:
        result = session.execute(
            text("SELECT * FROM doctors WHERE key_pass = :key"),
            {
                'key': data['key'],
            },
        ).fetchone()

        id = result['doctor_id']

        if result:
            return render_template('reset_pass_form.html', id=id, key=data['key'])
        else:
            return jsonify({'errors': 'Invalid key'}), 400
        
    except Exception as e:
        return jsonify({'errors': str(e)}), 500