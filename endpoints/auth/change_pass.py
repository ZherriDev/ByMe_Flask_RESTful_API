from flask import jsonify, request, Blueprint, render_template
from flask_mailman import EmailMultiAlternatives
from flask_jwt_extended import jwt_required, verify_jwt_in_request
from marshmallow import Schema, fields
from sqlalchemy import text
import bcrypt
from ..conn import Session

change_password_bp = Blueprint('change_password', __name__)

class ChangePasswordSchema(Schema):
    doctor_id = fields.Str(required=True)
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
    
    jwt_data = verify_jwt_in_request()

    jti = jwt_data['jti']
    session = Session()

    try:
        result_old_pass = session.execute(text('SELECT password FROM doctors WHERE doctor_id = :doctor_id'),
            {
                'doctor_id': data['doctor_id'],
            },
        ).fetchone()
        
        if bcrypt.checkpw(data['old_password'].encode('utf8'), result_old_pass[0].encode('utf8')):
            session.execute(
                text('UPDATE doictors SET password = :password WHERE doctor_id = :doctor_id'),
                {
                    'doctor_id': data['doctor_d'],
                },
            )
            session.commit()
        
            
            session.execute(text('UPDATE sessions SET in_blacklist = 1 WHERE doctor_id = :doctor_id'),
                {
                    'doctor_id': data['doctor_id'],
                },
            )

            session.commit()
        
            return jsonify({'success': True}), 200    
        else:
            return jsonify({'message': 'Invalid old password'}), 400
        
    except Exception as e:
        session.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        session.close()
    
