from flask import jsonify, request, Blueprint, render_template
from flask_jwt_extended import jwt_required, verify_jwt_in_request, decode_token
from flask_mailman import EmailMultiAlternatives
from marshmallow import Schema, fields
from sqlalchemy import text
import bcrypt
import hashlib
from ..conn import Session

logout_bp = Blueprint('logout_bp', __name__)

@logout_bp.route('/logout', methods=['DELETE'])
@jwt_required()
def logout():
    
    jwt_data = verify_jwt_in_request()
    
    jti = jwt_data[1]['jti']

    try:
        session = Session()

        session.execute(
            text("UPDATE sessions SET in_blacklist = 1 WHERE jti = :jti"),
            {
                'jti': jti,
            },
        )
        session.commit()
        return jsonify({'success': True}), 200
    except Exception as e:
        session.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        session.close()