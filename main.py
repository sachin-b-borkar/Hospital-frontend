import os
from flask import Flask,request,jsonify,render_template,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api,Resource
from http import HTTPStatus
from flask_migrate import Migrate

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:welcome$1234@localhost/hospital"
db = SQLAlchemy(app)
migrate = Migrate(app,db)

class Hospital1(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # this is the primary key
    name = db.Column(db.String(80), nullable=False)
    phone_number = db.Column(db.Integer, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    bed_type = db.Column(db.String(80), nullable=False)
    address = db.Column(db.String(80), nullable=False)
    state = db.Column(db.String(80), nullable=False)
    city = db.Column(db.String(80), nullable=False)
    patient_status = db.Column(db.String(80), nullable=False)

    # add patient
    @staticmethod
    def register_patient(name, phone_number, age ,bed_type,address,state,city,patient_status):
        print("register method")
        new_user= Hospital1(name=name, phone_number=phone_number, age=age , bed_type=bed_type ,address=address,state=state,city=city,patient_status=patient_status)
        print(new_user)
        result = db.session.add(new_user)
        print(result)
        db.session.commit()
        return result

    # get patient details
    @staticmethod
    def get_all_patient():
        return Hospital1.query.all()

    # get patient details by number
    @staticmethod
    def get_patient_by_phone(phone_number):
        return Hospital1.query.filter_by(phone_number=phone_number).first()

    # delete patient details by number
    @staticmethod
    def delete_patient(id):
        delete_user = Hospital1.query.filter_by(id=id).delete()
        print(delete_user)
        db.session.commit()
        return delete_user

    @staticmethod
    def update_user(id, address, age, bed_type , state ,city, patient_status):
        update_user = Hospital1.query.filter_by(id=id).first()
        print(update_user)
        update_user.address = address
        update_user.age = age
        update_user.bed_type = bed_type
        update_user.state = state
        update_user.city = city
        update_user.patient_status = patient_status
        db.session.commit()
        return update_user

@app.route("/", methods= ["GET","POST"])
def homepage():
    if request.method == "GET":
        return render_template("home.html")
    else:
        if request.method =="POST":
            return redirect(url_for("register_patient"))


@app.route("/getpatient",methods=["GET"] )
def get_All_Patient():
    data = Hospital1.get_all_patient()
    # print(data)
    # patient_list= []
    # for i in data:
    #     temp_dict= { 'id':i.id ,'name':i.name, 'phone_number': i.phone_number, 'age':i.age ,'bed_type': i.bed_type,
    #                   'address': i.address , 'state':i.state ,'city': i.city, 'patient_status':i.patient_status }
    #     patient_list.append(temp_dict)
    return render_template("getpatient.html",data=data)

@app.route("/register", methods=["GET","POST"])
def register_patient():
    if request.method == "GET":
        print("get method")
        return render_template("register.html",flag=False)
    else:
        if request.method == "POST":
            print("post method")
            name = request.form["name"]
            phone_number=request.form["phone_number"]
            age = request.form["age"]
            bed_type = request.form["bed_type"]
            address = request.form["address"]
            state = request.form["state"]
            city = request.form["city"]
            patient_status = request.form["patient_status"]
            check_user = Hospital1.get_patient_by_phone(phone_number=phone_number)
            print(check_user)
            try:
                if check_user:
                    return  "<h3>Patient Deatils Present </h3>"
                else:
                    add_entry= Hospital1.register_patient(name=name, phone_number=phone_number, age=age ,bed_type=bed_type,address=address,state=state,city=city,patient_status=patient_status)
                    return render_template("register.html",flag=True)
            except:
                return "Invalid Entry"

@app.route("/deletepatient", methods=["GET","DELETE"] )
def delete_Patient():
    if request.method == "GET":
        print("get method")
        return render_template("delete.html")
    else:
            if request.method == "DELETE":
                data = Hospital1.delete_patient(id=id)
                print(data)
                if data:
                    return HTTPStatus.OK
                else:
                    return HTTPStatus.NOT_FOUND


app.run(port=5007)
