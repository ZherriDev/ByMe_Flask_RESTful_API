from flask import Flask, render_template, jsonify
from flask_jwt_extended import JWTManager, jwt_required
from sqlalchemy import text
from endpoints.conn import Session
from flask_mailman import Mail, EmailMultiAlternatives

from endpoints.auth.register import register_bp
from endpoints.auth.login import login_bp
from endpoints.auth.confirm_email import confirm_email_bp
from endpoints.auth.logout import logout_bp
from endpoints.auth.request_reset_pass import request_reset_pass_bp
from endpoints.auth.reset_pass import reset_pass_bp
from endpoints.auth.reset_pass_form import reset_pass_form_bp

from endpoints.doctor.select_doctor import select_doctor_bp
from endpoints.doctor.select_doctor_id import select_doctor_id_bp
from endpoints.doctor.delete_doctor import delete_doctor_bp
from endpoints.doctor.update_doctor import update_doctor_bp

from endpoints.module.delete_module import delete_module_bp
from endpoints.module.select_module import select_module_bp
from endpoints.module.select_module_id import select_module_id_bp
from endpoints.module.insert_module import insert_module_bp
from endpoints.module.update_module import update_module_bp

from endpoints.patient.insert_patient import insert_patient_bp
from endpoints.patient.update_patient import update_patient_bp
from endpoints.patient.delete_patient import delete_patient_bp
from endpoints.patient.select_patient import select_patient_bp
from endpoints.patient.update_patient_doctor import update_patient_doctor_bp

app = Flask(__name__)

app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'cinesquadd@gmail.com'
app.config['MAIL_PASSWORD'] = 'pbeu qgam kcpn gchv'

mail = Mail(app)

app.config['JWT_SECRET_KEY'] = '5#$*e;phl"n£zRz@s1A#ki%Z{I.x=wzO+cdF~£`+8xK?<JZ6zA'

jwt = JWTManager(app)

@jwt.token_in_blocklist_loader
def check_if_token_in_blacklist(jwt_header, jwt_data):
    jti = jwt_data['jti']

    session = Session()

    result = session.execute(
        text("SELECT in_blacklist FROM sessions WHERE jti = :jti"),
        {'jti': jti},
    ).fetchone()

    if result[0] == 1:
        return True
    else:
        return False
        
app.register_blueprint(register_bp, url_prefix='/auth')
app.register_blueprint(login_bp, url_prefix='/auth')
app.register_blueprint(confirm_email_bp, url_prefix='/auth')
app.register_blueprint(logout_bp, url_prefix='/auth')
app.register_blueprint(request_reset_pass_bp, url_prefix='/auth')
app.register_blueprint(reset_pass_bp, url_prefix='/auth')
app.register_blueprint(reset_pass_form_bp, url_prefix='/auth')

app.register_blueprint(select_doctor_bp, url_prefix='/doctor')
app.register_blueprint(select_doctor_id_bp, url_prefix='/doctor')
app.register_blueprint(delete_doctor_bp, url_prefix='/doctor')
app.register_blueprint(update_doctor_bp, url_prefix='/doctor')

app.register_blueprint(delete_module_bp, url_prefix='/module')
app.register_blueprint(select_module_bp, url_prefix='/module')
app.register_blueprint(select_module_id_bp, url_prefix='/module')
app.register_blueprint(insert_module_bp, url_prefix='/module')
app.register_blueprint(update_module_bp, url_prefix='/module')

app.register_blueprint(insert_patient_bp, url_prefix='/patient')
app.register_blueprint(select_patient_bp, url_prefix='/patient')
app.register_blueprint(update_patient_bp, url_prefix='/patient')
app.register_blueprint(delete_patient_bp, url_prefix='/patient')
app.register_blueprint(update_patient_doctor_bp, url_prefix='/patient')

@app.route('/', methods=['GET'])
def index():
    return 'Olá'

if __name__ == '__main__':
    app.run(port=5000, host='localhost', debug=False)
