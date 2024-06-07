# ByMe Flask RESTful API
[![Python](https://skillicons.dev/icons?i=python)](https://en.wikipedia.org/wiki/Python_(programming_language))
[![HTML](https://skillicons.dev/icons?i=html)](https://en.wikipedia.org/wiki/HTML)
[![Flask](https://skillicons.dev/icons?i=flask)](https://en.wikipedia.org/wiki/Flask_(web_framework))
[![Django](https://skillicons.dev/icons?i=django)](https://en.wikipedia.org/wiki/Django_(web_framework))
[![MySQL](https://skillicons.dev/icons?i=mysql)](https://en.wikipedia.org/wiki/MySQL)
[![Postman](https://skillicons.dev/icons?i=postman)](https://en.wikipedia.org/wiki/Postman_(software))

## ℹ About the Project
This project was developed during our internship at the company ByMe - Information Technology, Lda. based in Porto, Portugal.

This was our first experience having contact with slightly more complex projects like this. This Flask API is just the back-end of the project, 
the front-end is found in this organization's repository:
[ByMe_Flutter_App](https://github.com/byme-internship-project/ByMe_Flutter_APP)

The main objective of the API is to provide a robust and scalable interface for managing clinical data such as patient information, appointment scheduling, and medical records. 
The API facilitates communication between the mobile application developed in Flutter and the server, ensuring that data is transferred quickly and securely.

## ✏️ Authors
- [RaveDev](https://github.com/Ravejaja)
- [ZherriDev](https://github.com/ZherriDev)

## 🔗 Endpoints
### Admin:
- [GET] **/admin/shutdown** - Shut down the server only if the author of the request is an administrator.
### Appointments:
- [GET] **/appointments/select_appointments/query/date/time** - Selects appointments for the day or days after the chosen day and time.
- [POST] **/appointments/insert_appointments** - Insert an appointment with the doctor ID, patient ID, appointment subject, date and time.
- [DELETE] **/appointments/delete_appointment** - Deletes an appointment by receiving the appointment ID.
### Authentication:
- [POST] **/auth/register** - Register a new doctor with full name, specialty, email and password.
- [GET] **/auth/confirm_email/key** - Validates the key to confirm the registered email.
- [POST] **/auth/login** - Log in with the doctor's email and password, taking the user's public IP, device name, operating system and location.
- [POST] **/auth/request_reset_pass** - Make a password reset request if the doctor has forgotten it, the endpoint receives the account email for association.
- [GET] **/auth/reset_pass/key** - Validates the key to reset the account password.
- [POST] **/auth/reset_pass_form** - Resets the account password. Receive the doctor ID, new password and key for verification.
- [POST] **/auth/change_email** - Change the doctor's email, receiving the doctor ID, old email and new email.
- [POST] **/auth/change_password** - Change the doctor's password, receiving the doctor ID, old password and new password.
- [DELETE] **/auth/logout** - Logs the doctor out, receiving the doctor's current token to add him to the blacklist.
### Doctor:
- [GET] **/doctor/select_doctors/search** - Selects multiple doctors as a search engine.
- [GET] **/doctor/select_doctor/id** - Select a single doctor using doctor ID.
- [PATCH] **/doctor/update_doctor** - Update the doctor's data with your ID and all details, fullname, profile photo, telephone number, sex, birthdate, address, speciality.
- [DELETE] **/doctor/delete_doctor** - Deletes a doctor by receiving the doctor ID.
### Module:
- [GET] **/module/select_modules/id** - Selects all modules for a patient with their ID.
- [GET] **/module/select_module/id** - Selects a module with the module ID.
- [POST] **/module/insert_module** - Insert a module for a patient with its ID and data, episode, module and status.
- [PATCH] **/module/update_module** - Updates a module's data with its ID. Updates only the episode and module.
- [PATCH] **/module/update_module_status** - Updates the status of a module with its ID.
- [DELETE] **/module/delete_module** - Deletes a module with its ID.
### Patient:
- [GET] **/patient/select_patients/id/search/order/state** - Selects all patients for a doctor with their ID as a search engine, the search, show order and patient state.
- [GET] **/patient/select_patient/id** - Selects a patient with the patient ID.
- [POST] **/patient/insert_patient** - Insert a patient for a doctor with its ID and data, name, telephone number, email, sex, birthdate, process number, address, postal code, town, nif, sns, status.
- [PATCH] **/patient/update_patient** - Updates a patient's data with its ID. Updates all insertion data except status.
- [PATCH] **/patient/update_patient_status** - Updates the status of a patient with its ID.
- [PATCH] **/patient/update_patient_doctor** - Updates a patient's doctor with their ID, transferring it to that doctor.
- [DELETE] **/patient/delete_patient** - Deletes a patient with its ID.
### Sessions:
- [GET] **/sessions/select_sessions/id** - Selects all sessions for a doctor with their ID.
- [PATCH] **/sessions/update_session** - Blacklist a session.

## 🗄️ Database Schema
![byme_project_db_schema](https://github.com/byme-internship-project/ByMe_Flask_RESTful_API/assets/165341887/7fcc8767-dbc4-48db-83b2-6fc087eaec00)

## ❗Support
Please [create a new issue](https://github.com/byme-internship-project/ByMe_Flask_RESTful_API/issues/new) if you have a suggestion or if you found a problem.
