#!/usr/bin/env python3

from flask import Flask, make_response, request, jsonify, render_template, send_from_directory
from prometheus_flask_exporter import PrometheusMetrics
from flask_migrate import Migrate
from flask_restful import Api, Resource
from werkzeug.exceptions import NotFound
import os
# from flask_Bcrypt import Bcrypt
from dotenv import load_dotenv
load_dotenv()

from models import db, User, Appointment, Patient,Staff

app = Flask(
    __name__,
    static_url_path='/',
    static_folder='../frontend/build',
    template_folder='../frontend/build'
    )
# bcrypt= Bcrypt(app)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hospital.db'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'

metrics = PrometheusMetrics(app)

migrate = Migrate(app, db)

db.init_app(app)
api= Api(app)

@app.errorhandler(NotFound)
def handle_not_found(e):
    return render_template('index.html', title='Homepage', message='Welcome to our website!')




# class Index(Resource):
#     def index(self):
#         return render_template('index.html', title='Homepage', message='Welcome to our website!')

# api.add_resource(Index, '/')


class PatientData(Resource): 
    def get(self):
        all_patients= Patient.query.all()
        patient_dict= [patient.to_dict() for patient in all_patients]
        response= make_response(jsonify(patient_dict), 200)
        return response
   
    def post(self):
        data= request.get_json()
        name= data.get('name')
        age= data.get ('age')
        gender= data.get('gender')
        contact_number= data.get('contact_number')
        email = data.get('email')
        date_of_birth = data.get('date_of_birth')
        try:
            new_patient= Patient(name = name, age = age, gender = gender, contact_number = contact_number, email = email, date_of_birth = date_of_birth)
            db.session.add(new_patient)
            db.session.commit()

            new_patient_dict= new_patient.to_dict()
            response = make_response(jsonify(new_patient_dict), 200)
            return response
        except Exception as e:
            response= make_response({'error': str(e)}, 400)
            return response

api.add_resource(PatientData, '/patients')

class PatientByID(Resource):
    def get(self, id):
        patient = Patient.query.filter_by(id=id).first()
        patient_dict = patient.to_dict()

        response = make_response(
            jsonify(patient_dict),
            200
        )
        return response 
    
    def delete(self,id):
        patient = Patient.query.filter_by(id=id).first()
        db.session.delete(patient)
        db.session.commit()
        response = make_response(jsonify({"Message":"Deleted Successfully"}), 200)
        return response

api.add_resource(PatientByID, '/patients/<int:id>')


class StaffData(Resource): 
    def get(self):
        all_staffs= Staff.query.all()
        staff_dict= [staff.to_dict() for staff in all_staffs]
        response= make_response(jsonify(staff_dict), 200)
        return response
   
    def post(self):
        data= request.get_json()
        name= data.get('name')
        specialisation= data.get ('specialisation')
        start_date= data.get('start_date')
        end_date= data.get('end_date')
        contact_number= data.get('contact_number')
        email = data.get('email')
        status = data.get('status')
        try:
            new_staff= Staff(name = name, specialisation= specialisation, start_date = start_date, end_date = end_date, contact_number = contact_number, email = email, status = status)
            db.session.add(new_staff)
            db.session.commit()

            new_staff_dict= new_staff.to_dict()
            response = make_response(jsonify(new_staff_dict), 200)
            return response
        except Exception as e:
            response= make_response({'error': str(e)}, 400)
            return response

api.add_resource(StaffData, '/staffs')

class StaffByID(Resource):
    def get(self, id):
        staff = Staff.query.filter_by(id=id).first()
        staff_dict = staff.to_dict()

        response = make_response(
            jsonify(staff_dict),
            200
        )
        return response 
    
    def delete(self,id):
        staff = Staff.query.filter_by(id=id).first()
        db.session.delete(staff)
        db.session.commit()
        response = make_response(jsonify({"Message":"Deleted Successfully"}), 200)
        return response

api.add_resource(StaffByID, '/staffs/<int:id>')



class AppointmentData(Resource): 
    def get(self):
        all_appointments= Appointment.query.all()
        appointment_dict= [appointment.to_dict() for appointment in all_appointments]
        response= make_response(jsonify(appointment_dict), 200)
        return response
   
    def post(self):
        data= request.get_json()
        appointment_type= data.get ('appointment_type')
        appointment_date= data.get('appointment_date')
        patient_id =  data.get('patient_id')
        staff_id = data.get('staff_id')

        try:
            new_appointment= Appointment(appointment_type = appointment_type, appointment_date= appointment_date, patient_id = patient_id, staff_id= staff_id)
            db.session.add(new_appointment)
            db.session.commit()

            new_appointment_dict= new_appointment.to_dict()
            response = make_response(jsonify(new_appointment_dict), 200)
            return response
        except Exception as e:
            response= make_response({'error': str(e)}, 400)
            return response

api.add_resource(AppointmentData, '/appointments')

class AppointmentByID(Resource):
    def get(self, id):
        appointment = Appointment.query.filter_by(id=id).first()
        appointment_dict = appointment.to_dict()

        response = make_response(
            jsonify(appointment_dict),
            200
        )
        return response 
    
    def patch(self, id):
        appointment = Appointment.query.get(id)
        
        # appointment.appointment_date= date
        if not appointment:
            error_dict=  {'error': 'Appointment not found'}
            response= make_response(error_dict, 404)
            return response
        #    for attr, value in data.items():
        #         setattr(appointment, attr, value)
        data= request.get_json()
        date= data['dbDate']
        if date:
            appointment.appointment_date= date
            # db.session.add(appointment)
            db.session.commit()
            appointment_dict= appointment.to_dict()
            response= make_response(jsonify(appointment_dict), 200)
            return response 


    def delete(self,id):
        appointment = Appointment.query.filter_by(id=id).first()
        db.session.delete(appointment)
        db.session.commit()
        response = make_response(jsonify({"Message":"Deleted Successfully"}), 200)
        return response

api.add_resource(AppointmentByID, '/appointments/<int:id>')



#Login user
class Login(Resource):
    def post(self):
        data= request.get_json()
        username= data.get('username')
        password= data.get ('password')
        try:
            user= User.query.filter_by(username==username).first()
            if password==user.password:
                session['user_id']= user.id
                return user.to_dict(),200
        except Exception as e:
            response= make_response({'error': str(e)}, 400)
            return response

api.add_resource(Login, '/login')

#Sign UP User
class SignUp(Resource):
    def post(self):
        data= request.get_json()
        username= data.get('username')
        password= data.get ('password')
        role = data.get('role')
        #Checking if the user already exists in the database or not
        if  User.query.filter_by(username=username).first():
            response = make_response(jsonify({"Error":"User already exists"}), 200)
            return response
            post(self)
        
        elif User.query.filter_by(password=password).first():
            response = make_response(jsonify({"Error":"Password already exists"}), 200)
            return response
            post(self)
        else:
            new_user= User(username = username, password= password, role = role)
            db.session.add(new_user)
            db.session.commit()

            new_user_dict= new_user.to_dict()
            response = make_response(jsonify(new_user_dict), 200)
            return response

api.add_resource(SignUp, '/signup')


#Stay logged in
class CheckSessiom(Resource):
    def get (self):
        user= User.query.filter_by(User.id== session.get('user_id')).first()
        if user is None:
            abort(401) # Unauthorized
        else :
            return jsonify(user.to_dict ()) ,200

api.add_resource(CheckSessiom,'/checkSession')

#Log out
class Logout(Resource):
    def  get(self):
        session['user_id']=None
        return {'message':'logged out'}

api.add_resource(Logout,"/logout")

# Catch-all route to serve React frontend routes
@app.route('/')
@app.route('/<path:path>')
def serve(path=''):
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000)

