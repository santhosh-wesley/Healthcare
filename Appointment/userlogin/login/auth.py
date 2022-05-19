from flask import Blueprint, render_template, request,  redirect, url_for, flash
from .models import Admin, User
from werkzeug.security import generate_password_hash, check_password_hash
from .models import db
from flask_login import login_user, login_required, logout_user, current_user
import re
from flask import session



auth = Blueprint('auth', __name__)


@auth.route('/cust')
def cust():
    return render_template('cust_homepage.html')

@auth.route('/admin')
def adm():
    return render_template('admin_homepage.html')


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        admin = Admin.query.filter_by(email=email)
        if admin:
            if email=='admin@hospital.com' and password=='password':
                return redirect(url_for('auth.adm'))
     
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('auth.cust_homepage'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')
    return render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        name = request.form.get('Name')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        if (email == "" or name == "" or password1 == "" or password2 == ""):
            flash('Fields cannot be empty.', category='error')

        elif user:
            flash('Email already exists.', category='error')
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            flash('Invalid email address.', category='error')
        elif not re.match(r'[A-Za-z]+', name):
            flash('First name must contain only characters.', category='error')
        elif len(password1) < 8:
            flash('Password must be atleast 8 characters.', category='error')
        elif len(password1) > 20:
            flash('Password must be less than 20 characters.', category='error')
        elif re.search('[0-9]', password1) is None:
            flash('Password must have a number in it.', category='error')
        elif re.search('[A-Z]', password1) is None:
            flash('Password must have a capital letter.', category='error')

        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')

        else:
            new_user = User(email=email, first_name=name, password=generate_password_hash(
                password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('view.home'))

    return render_template("sign_up.html", user=current_user)
