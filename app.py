from flask import Flask, jsonify, request
from marshmallow import Schema, fields
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import bcrypt

app = Flask(__name__)

user_db = 'root'
password_db = 'root'
host_db = 'localhost'
database_db = 'teste'

engine = create_engine(f'mysql+pymysql://{user_db}:{password_db}@{host_db}/{database_db}')
Session = sessionmaker(bind=engine)

class UserSchema(Schema):
    name = fields.Str(required=True)
    email = fields.Email(required=True)
    password = fields.Str(required=True)

#!   R   E   G   I   S   T   E   R
@app.route('/register', methods = ['POST'])
def register_user():
    data = request.get_json()
    schema = UserSchema()
    errors = schema.validate(data)
    
    if errors:
        return jsonify({'errors': errors}), 400
    
    session = Session()
    
    try:
        salt = bcrypt.gensalt()
        hash_password = bcrypt.hashpw(data['password'].encode('utf8'), salt)
        session.execute(
            text("INSERT INTO usuarios (nome, email, senha, salt_senha) VALUES (:nome, :email, :senha, :salt_senha)"),
            {'nome': data['name'], 'email': data['email'], 'senha': hash_password, 'salt_senha': salt},
        )
        session.commit()
        return jsonify({'success': True}), 201
    except Exception as e:
        session.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        session.close()
        
if __name__ == '__main__':
    app.run(port=5000, host='localhost', debug=False)
