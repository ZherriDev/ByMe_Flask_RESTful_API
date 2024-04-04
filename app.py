from flask import Flask, jsonify, request
from marshmallow import Schema, fields
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import bcrypt

app = Flask(__name__)

user_db = 'sql11696357'
password_db = 'Qp4hRnMDZY'
host_db = 'sql11.freesqldatabase.com'
port_db = 3306
database_db = 'sql11696357'

engine = create_engine(f'mysql+pymysql://{user_db}:{password_db}@{host_db}:{port_db}/{database_db}')
Session = sessionmaker(bind=engine)

class LoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True)

class SelectDoctorSchema(Schema):
    search = fields.Str(required=True)

class SelectDoctorIDSchema(Schema):
    doctor_id = fields.Int(required=True)

class DeleteDoctorSchema(Schema):
    doctor_id = fields.Int(required=True)

class UpdateDoctorSchema(Schema):
    id = fields.Int(required=True)
    fullname = fields.Str(required=True)
    telephone = fields.Int(required=True)
    sex = fields.Str(required=True)
    birthdate = fields.Date(required=True)
    address = fields.Str(required=True)
    speciality = fields.Str(required=True)

class InsertPatientSchema(Schema):
    doctor_id = fields.Int(required=True)
    name = fields.Str(required=True)
    telephone = fields.Int(required=True)
    email = fields.Str(required=True)
    sex = fields.Str(required=True)
    birthdate = fields.Date(required=True)
    processnumber = fields.Int(required=True)
    address = fields.Str(required=True)
    postalcode = fields.Str(required=True)
    town = fields.Str(required=True)
    nif = fields.Int(required=True)
    sns = fields.Int(required=True)
    
class UpdatePatientSchema(Schema):
    patient_id = fields.Int(required=True)
    doctor_id = fields.Int(required=True)
    name = fields.Str(required=True)
    telephone = fields.Int(required=True)
    email = fields.Str(required=True)
    sex = fields.Str(required=True)
    birthdate = fields.Date(required=True)
    processnumber = fields.Int(required=True)
    address = fields.Str(required=True)
    postalcode = fields.Str(required=True)
    town = fields.Str(required=True)
    nif = fields.Int(required=True)
    sns = fields.Int(required=True)
    
class DeletePatientSchema(Schema):
    patient_id = fields.Int(required=True)

class ShowPatientSchema(Schema):
    doctor_id = fields.Int(required=True)
    order = fields.Str(required=False)
    state = fields.Str(required=False)   

@app.route('/', methods=['GET'])
def index():
    return 'Olá'

#!   L   O   G   I   N
@app.route('/login', methods = ['POST'])
def login_user():
    data = request.get_json()
    schema = LoginSchema()
    errors = schema.validate(data)
    
    if errors:
        return jsonify({'errors': errors}), 400
    
    session = Session()
    
    try:
        result = session.execute(
            text("SELECT * FROM doctors WHERE email = :email"),
            {'email': data['email']},
        ).fetchone()
        
        if result:
            if bcrypt.checkpw(data['password'].encode('utf8'), result['password'].encode('utf8')):
                return jsonify({'success': True, 'user': result}), 200
            else:
                return jsonify({'error': 'Palavra-passe incorreta'}), 400
        else:
            return jsonify({'error': 'Utilizador não encontrado'}), 400
    except Exception as e:
        session.rollback()
        return jsonify({'error': str(e)}), 500

#!   S   E   L   E   C   T   -   D   O   C   T   O   R
@app.route('/select_doctor', methods=['GET'])
def select_doctor():
    data = request.get_json()
    schema = SelectDoctorSchema()
    errors = schema.validate(data)

    if errors:
        return jsonify({'errors': errors}), 400
    
    session = Session()
    
    try:
        result = session.execute(
            text('SELECT * FROM doctors WHERE fullname LIKE "%:search%" OR speciality LIKE "%:search%" ORDER BY name ASC'),
            {'search': data['search']}
        ).fetchall()
        return jsonify({'success': True, 'doctors': result}), 200
    except Exception as e:
        session.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        session.close()

#!   S   E   L   E   C   T   -   D   O   C   T   O   R   -   I   D
@app.route('/select_doctor_id', methods=['GET'])
def select_doctor_id():
    data = request.get_json()
    schema = SelectDoctorIDSchema()
    errors = schema.validate(data)

    if errors:
        return jsonify({'errors': errors}), 400
    
    
    

#!   D   E   L   E   T   E   -   D   O   C   T   O   R
@app.route('/delete_doctor', methods=['DELETE'])
def delete_doctor():
    data = request.get_json()
    schema = DeleteDoctorSchema()
    errors = schema.validate(data)

    if errors:
        return jsonify({'errors': errors}), 400
    
    session = Session()
    
    try:
        session.execute(
            text("DELETE FROM doctors WHERE doctor_id = :id"),
            {'id': data['id']},
        )
        session.commit()
        return jsonify({'success': True}), 200
    except Exception as e:
        session.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        session.close()

#!   U   P   D   A   T   E   -   D   O   C   T   O   R
@app.route('/update_doctor', methods=['UPDATE'])
def update_doctor():
    data = request.get_json()
    schema = UpdateDoctorSchema()
    errors = schema.validate(data)
    
    if errors:
        return jsonify({'errors': errors}), 400
    
    session = Session()
    
    try:
        result = session.execute(
            text('UPDATE doctors SET fullname = :fullname, telephone = :telephone, sex = :sex, \
                birthdate = :birthdate, address = :address, speciality = :speciality WHERE doctor_id = :id'),
            {
                'fullname': data['fullname'], 
                'telephone': data['telephone'], 
                'sex': data['sex'], 
                'birthdate': data['birthdate'], 
                'address': data['address'], 
                'speciality': data['speciality'], 
                'id': data['id']}
        )
        session.commit()
        return jsonify({'success': True}), 200
    except Exception as e:
        session.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        session.close()

#!   I   N   S   E   R   T   -   P   A   T   I   E   N   T
@app.route('/insert_patient', methods=['POST'])
def insert_patient():
    data = request.get_json()
    schema = InsertPatientSchema()
    errors = schema.validate(data)

    if errors:
        return jsonify({'errors': errors}), 400
    
    session = Session()
    try:
        session.execute(
            text("INSERT INTO patients (name, telephone, email, sex, birthdate, address, postalcode, town, nif, \
                sns, doctor_id, processnumber, admission_date) VALUES (:name, :telephone, :email, :sex, :birthdate, :address, :postcode, \
                :town, :nif, :sns, :doctor_id, :processnumber, :admission_date)"),
            {
                'name': data['name'], 
                'telephone': data['telephone'],
                'email': data['email'],
                'sex': data['sex'], 
                'birthdate': data['birthdate'], 
                'address': data['address'], 
                'postalcode': data['postalcode'], 
                'town': data['town'], 
                'nif': data['nif'], 
                'sns':data['sns'],
                'doctor_id': data['doctor_id'],
                'processnumber': data['processnumber'],
                'admission_date': datetime.now()
            },
            
        )
        session.commit()
        return jsonify({'success': True}), 201
    except Exception as e:
        session.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        session.close()

#!   U   P   D   A   T   E   -   P   A   T   I   E   N   T
@app.route('/update_patient', methods=['POST'])
def update_patient():
    data = request.get_json()
    schema = UpdatePatientSchema()
    errors = schema.validate(data)

    if errors:
        return jsonify({'errors': errors}), 400
    
    session = Session()
    
    try:
        select = session.execute(
            text('SELECT doctor_id FROM doctors WHERE patient_id = :patient_id'),
            {'patient_id': data['patient_id']}
        ).fetchone()
        
        result = session.execute(
            text('UPDATE patients SET doctor_id = :doctor_id, name = :name, telephone = :telephone, email = :email, \
                sex = :sex, birthdate = :birthdate, processnumber = :processnumber, address = :address, \
                postalcode = :postalcode, town = :town, nif = :nif, sns = :sns WHERE patient_id = :patient_id'),
            {
                'doctor_id': data['doctor_id'], 
                'name': data['name'], 
                'telephone': data['telephone'], 
                'email': data['email'],
                'sex': data['sex'], 
                'birthdate': data['birthdate'], 
                'processnumber': data['processnumber'], 
                'address': data['address'],
                'postalcode': data['postalcode'], 
                'town': data['town'], 
                'nif': data['nif'], 
                'sns': data['sns'], 
                'patient_id': data['patient_id'],
            }
        )
        session.commit()
        return jsonify({'success': True}), 200
    except Exception as e:
        session.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        session.close()

#!   D   E   L   E   T   E   -   P   A   T   I   E   N   T
@app.route('/delete_patient', methods=['DELETE'])
def delete_patient():
    data = request.get_json()
    schema = DeletePatientSchema()
    errors = schema.validate(data)

    if errors:
        return jsonify({'errors': errors}), 400
    
    session = Session()
    
    try:
        session.execute(
            text("DELETE FROM patients WHERE patient_id = :id"),
            {'id': data['patient_id']},
        )
        session.commit()
        return jsonify({'success': True}), 200
    except Exception as e:
        session.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        session.close()

@app.route('/show_patients', methods=['GET'])
def show_patients():

    data = request.get_json()
    schema = ShowPatientSchema()
    errors = schema.validate(data)
    
    session = Session()

    if errors:
        return jsonify({'errors': errors}), 400
        
    try:
        result = session.execute(
            text("SELECT * FROM patients WHERE doctor_id = :doctor_id"),
            {'doctor_id': data['doctor_id']}
        ).fetchall()
        return jsonify({'success': True, 'patients': result}), 200
    except Exception as e:
        session.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        session.close()

if __name__ == '__main__':
    app.run(port=5000, host='localhost', debug=False)
