from flask import Flask, render_template, jsonify, request
from flask_jwt_extended import JWTManager, jwt_required
from sqlalchemy import text
from endpoints.conn import Session
from flask_mailman import Mail
from endpoints.utils import set_app
import os
from dotenv import load_dotenv

from endpoints.admin.shutdown import shutdown_bp

from endpoints.appointments.delete_appointments import delete_appointments_bp
from endpoints.appointments.insert_appointments import insert_appointments_bp
from endpoints.appointments.select_appointments import select_appointments_bp

from endpoints.auth.register import register_bp
from endpoints.auth.login import login_bp
from endpoints.auth.confirm_email import confirm_email_bp
from endpoints.auth.change_email import change_email_bp
from endpoints.auth.logout import logout_bp
from endpoints.auth.request_reset_pass import request_reset_pass_bp
from endpoints.auth.reset_pass import reset_pass_bp
from endpoints.auth.reset_pass_form import reset_pass_form_bp
from endpoints.auth.change_pass import change_password_bp

from endpoints.doctor.select_doctors import select_doctors_bp
from endpoints.doctor.select_doctor_id import select_doctor_id_bp
from endpoints.doctor.delete_doctor import delete_doctor_bp
from endpoints.doctor.update_doctor import update_doctor_bp

from endpoints.module.delete_module import delete_module_bp
from endpoints.module.select_module import select_module_bp
from endpoints.module.select_module_id import select_module_id_bp
from endpoints.module.insert_module import insert_module_bp
from endpoints.module.update_module import update_module_bp
from endpoints.module.update_module_status import update_module_status_bp

from endpoints.patient.insert_patient import insert_patient_bp
from endpoints.patient.update_patient import update_patient_bp
from endpoints.patient.delete_patient import delete_patient_bp
from endpoints.patient.select_patient_id import select_patient_id_bp
from endpoints.patient.select_patients import select_patients_bp
from endpoints.patient.update_patient_doctor import update_patient_doctor_bp
from endpoints.patient.update_patient_status import update_patient_status_bp

from endpoints.sessions.select_sessions import select_sessions_bp
from endpoints.sessions.update_session import update_session_bp

app = Flask(__name__)

load_dotenv()

app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
app.config['MAIL_PORT'] = os.getenv('MAIL_PORT')
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')

mail = Mail(app)

app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')

set_app(app)

@app.errorhandler(429)
def ratelimit_handler(_):
    body = {
        "error": "Too many requests"
    }
    return jsonify(body), 429

jwt = JWTManager(app)

@jwt.token_in_blocklist_loader
def check_if_token_in_blacklist(jwt_header, jwt_data):
    jti = jwt_data['jti']

    session = Session()

    result = session.execute(
        text("SELECT in_blacklist FROM sessions WHERE jti = :jti"),
        {'jti': jti},
    ).fetchone()

    if result:
        if result[0] == 1:
            return True
        else:
            return False
    else:
        return False

app.register_blueprint(shutdown_bp, url_prefix='/admin')

app.register_blueprint(delete_appointments_bp, url_prefix='/appointments')
app.register_blueprint(insert_appointments_bp, url_prefix='/appointments')
app.register_blueprint(select_appointments_bp, url_prefix='/appointments')

app.register_blueprint(register_bp, url_prefix='/auth')
app.register_blueprint(login_bp, url_prefix='/auth')
app.register_blueprint(confirm_email_bp, url_prefix='/auth')
app.register_blueprint(change_email_bp, url_prefix='/auth')
app.register_blueprint(logout_bp, url_prefix='/auth')
app.register_blueprint(request_reset_pass_bp, url_prefix='/auth')
app.register_blueprint(reset_pass_bp, url_prefix='/auth')
app.register_blueprint(reset_pass_form_bp, url_prefix='/auth')
app.register_blueprint(change_password_bp, url_prefix='/auth')

app.register_blueprint(select_doctors_bp, url_prefix='/doctor')
app.register_blueprint(select_doctor_id_bp, url_prefix='/doctor')
app.register_blueprint(delete_doctor_bp, url_prefix='/doctor')
app.register_blueprint(update_doctor_bp, url_prefix='/doctor')

app.register_blueprint(delete_module_bp, url_prefix='/module')
app.register_blueprint(select_module_bp, url_prefix='/module')
app.register_blueprint(select_module_id_bp, url_prefix='/module')
app.register_blueprint(insert_module_bp, url_prefix='/module')
app.register_blueprint(update_module_bp, url_prefix='/module')
app.register_blueprint(update_module_status_bp, url_prefix='/module')

app.register_blueprint(insert_patient_bp, url_prefix='/patient')
app.register_blueprint(select_patient_id_bp, url_prefix='/patient')
app.register_blueprint(select_patients_bp, url_prefix='/patient')
app.register_blueprint(update_patient_bp, url_prefix='/patient')
app.register_blueprint(delete_patient_bp, url_prefix='/patient')
app.register_blueprint(update_patient_doctor_bp, url_prefix='/patient')
app.register_blueprint(update_patient_status_bp, url_prefix='/patient')

app.register_blueprint(select_sessions_bp, url_prefix='/sessions')
app.register_blueprint(update_session_bp, url_prefix='/sessions')

@app.route('/', methods=['GET'])
def index():
    return 'Olá'

if __name__ == '__main__':
    app.run(port=5000, host='localhost', debug=False)
