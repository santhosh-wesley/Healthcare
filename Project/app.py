from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy 
import os

app = Flask(__name__)
app.secret_key = "Secret Key"

path = os.path.abspath( os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + os.path.join(path , 'test.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
''' if os isnot to be imported 
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///patients.sqlite3'
'''
db = SQLAlchemy(app)

class Appointment(db.Model):
    id = db.Column(db.Integer , primary_key = True)
    patient = db.Column(db.String(100))
    name = db.Column(db.String(100))
    phone = db.Column(db.String(100))
    email = db.Column(db.String(100))
    consultmed = db.Column(db.String(100))
    specialist = db.Column(db.String(100))
    practitioner = db.Column(db.String(100))
    date = db.Column(db.String(100))
    time = db.Column(db.String(100))


    def __init__(self, patient, name, phone, email, consultmed, specialist, practitioner, date, time):
        self.patient = patient
        self.name = name
        self.phone = phone
        self.email = email
        self.consultmed = consultmed
        self.specialist = specialist
        self.practitioner = practitioner
        self.date = date
        self.time = time
  
@app.route('/')
def BookAppoint():
    all_data = Appointment.query.all()
    return render_template("admin_homepage.html", all_data = all_data)

'''def Admin():
    
    return render_template("admin_homepage.html")'''


@app.route('/insert', methods = ['GET','POST'])
def insert():
    if request.method == 'POST':
        patient = request.form['patient']
        name = request.form['name']
        phone = request.form['phone']
        email = request.form['email']
        consultmed = request.form['consultmed']
        specialist = request.form['specialist']
        practitioner = request.form['practitioner']
        date = request.form['date']
        time = request.form['time']
        
		#check the validity of data 
        my_data = Appointment(patient, name, phone, email, consultmed, specialist, practitioner, date, time)
        db.session.add(my_data)
        db.session.commit()

        flash("Patient Details Inserted Successfully")
        return render_template('admin_homepage.html')
@app.route('/delete/<id>/')
def delete(id):
    my_data = Appointment.query.get(id)
    db.session.delete(my_data)
    db.session.commit()

    flash("Patient Data Deleted Successfully")
    return redirect(url_for('BookAppoint'))


if __name__ == "__main__":
    app.run(debug = True)