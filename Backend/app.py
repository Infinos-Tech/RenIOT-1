from flask import Flask, render_template, url_for, request, jsonify, g
from flask.helpers import flash
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required
from flask_wtf import FlaskForm
from sqlalchemy.orm import session
from flask.globals import session
from werkzeug.utils import redirect
from wtforms import StringField, PasswordField, SubmitField, IntegerField
from wtforms.validators import InputRequired, Length
import hashlib
from datetime import datetime
from random import *
from flask_mail import *
from flask_mail import Message
from flask_mail import Mail
import pymysql

pymysql.install_as_MySQLdb()

app = Flask(__name__, instance_relative_config=True)
CORS(app, resources={r"/*": {"origins": "*"}})

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:''@localhost/infinosbox'
# app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "shravanissshravanissshravaniss"

app.config["MAIL_SERVER"] = 'smtp.gmail.com'
app.config["MAIL_PORT"] = 465
app.config["MAIL_USERNAME"] = 'nreply760@gmail.com'
app.config['MAIL_PASSWORD'] = 'Vijay@26101996'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)
otp = randint(000000, 999999)

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "user"


@login_manager.user_loader
def load_user(user_id):
    return Useruthentication.query.get(int(user_id))


class Useruthentication(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column('userID', db.Integer, primary_key=True)
    mailid = db.Column('mailID', db.String(20))
    userpassword = db.Column('userPassword', db.String(40))
    username = db.Column('userName', db.String(40))
    phno = db.Column('phno', db.Integer)
    rectym = db.Column('recentLogTym', db.DateTime)

    def __init__(self, mailid, userpassword, username, phno, rectym):
        self.mailid = mailid
        self.userpassword = userpassword
        self.username = username
        self.phno = phno
        self.rectym = rectym


class Board(db.Model, UserMixin):
    __tablename__ = 'board'
    boardid = db.Column('boardID', db.Integer, primary_key=True)
    boardpassword = db.Column('boardPassword', db.String(33))


class WeatherData(db.Model, UserMixin):
    __tablename__ = 'weatherData'
    tempreature = db.Column('Tempreature', db.String(40))
    location = db.Column('Location', db.String(40))
    weatherdata = db.Column('weatherdata', db.String(40))

    def __init__(self, tempreature, location, weatherdata):
        self.tempreature = tempreature
        self.location = location
        self.weatherdata = weatherdata


# db.create_all()


class LoginForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=5, max=12)], render_kw={"placeholder": "Username"})
    userpassword = PasswordField(validators=[InputRequired(), Length(min=5, max=12)],
                                 render_kw={"placeholder": "Password"})
    submit = SubmitField("Login")


class BoxLoginForm(FlaskForm):
    boardid = IntegerField(validators=[InputRequired()], render_kw={"placeholder": "Board-Id"})
    boardpassword = PasswordField(validators=[InputRequired(), Length(min=4, max=12)],
                                  render_kw={"placeholder": "Board-Password"})
    submit = SubmitField("Login")


class SignUpForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=5, max=12)], render_kw={"placeholder": "Username"})
    phno = IntegerField(validators=[InputRequired()], render_kw={"placeholder": "Phone No"})
    mailid = StringField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Mail-Id"})
    userpassword = PasswordField(validators=[InputRequired(), Length(min=5, max=12)],
                                 render_kw={"placeholder": "Password"})
    submit = SubmitField("Register")


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/user', methods=["GET", "POST"])
def user():
    form = LoginForm()
    if form.validate_on_submit():
        us = hashlib.md5(form.username.data.encode())
        user = Useruthentication.query.filter_by(username=us.hexdigest()).first()
        md5 = hashlib.md5(form.userpassword.data.encode())
        if user and user.userpassword == md5.hexdigest():
            login_user(user)
            return redirect(url_for('dashboard'))
    return render_template('user.html', form=form)


@app.route('/dashboard', methods=["GET", "POST"])
@login_required
def dashboard():
    return render_template('dashboard.html')


@app.route('/signup', methods=["GET", "POST"])
def signup():
    form = SignUpForm()

    if form.validate_on_submit():
        un = hashlib.md5(form.username.data.encode())
        up = hashlib.md5(form.userpassword.data.encode())
        user = Useruthentication.query.filter_by(username=un.hexdigest()).first()
        if user:
            flash("username already taken! Try again!", "info")
            return redirect(url_for('signup'))
        else:
            newUser = Useruthentication(username=un.hexdigest(),
                                        phno=form.phno.data,
                                        mailid=form.mailid.data,
                                        userpassword=up.hexdigest(),
                                        rectym=datetime.now())
            db.session.add(newUser)
            db.session.commit()
            flash("Registration successful", "info")
            return redirect(url_for('user'))

    return render_template('signup.html', form=form)


# @app.route('/userSignUp', methods=["POST"])
# def UserSignUp():
#     if request.method == 'POST':
#         data = request.get_json()
#         print(data['username'])
#         print(data['password'])
#         print(data['email'])
#         print(data['phoneno'])
#         return jsonify({"message": "signup"}), 200


@app.route('/board', methods=["GET", "POST"])
@login_required
def board():
    form = BoxLoginForm()
    if form.validate_on_submit():
        user = Board.query.filter_by(boardid=form.boardid.data).first()
        md5 = hashlib.md5(form.boardpassword.data.encode())
        if user and user.boardpassword == md5.hexdigest():
            return "Box successfully logged in"
    return render_template('board.html', form=form)


@app.route('/boxSignUp', methods=["POST"])
def boardSignup():
    if request.method == 'POST':
        data = request.get_json()
        print(data['username'])
        print(data['password'])
        return jsonify({"message": "boxsignup"}), 200


# Forgot Password Functionality Goes From Here...
@app.route('/Get_OTP', methods=['GET', 'POST'])
def Get_OTP():
    if request.method == "POST":
        useremail = request.form.get("user")
        result = Useruthentication.query.filter_by(mailid=useremail).first()
        if result is not None:
            session["user"] = useremail
            msg = Message('OTP', sender='nreply760@gmail.com', recipients=[result.mailid])
            msg.body = f"Hello {result.username} a request has been recieved to change the password for your Account your secret otp is \n {str(otp)}"
            mail.send(msg)
            flash(f"hello {result.username} otp has been sent you registered email id {result.mailid}", "success")
            return render_template("otp_valid.html")
        else:
            flash("UserName Does Not Exists", "danger")

    return render_template("reset.html")


@app.route('/otp_validation', methods=['GET', 'POST'])
def otp_validation():
    if g.user:
        if request.method == "POST":
            user_otp = request.form.get("otp1")
            if user_otp == str(otp):
                return render_template("pw.html")
            else:
                flash("OTP doesn't Match", "danger")
                return render_template("otp_valid.html")


@app.route('/Password_Update', methods=['GET', 'POST'])
def Password_Update():
    # Password encrypted Before Updating.
    if g.user:
        if request.method == "POST":
            ps = hashlib.md5(request.form.get("ps").encode())
            ps1 = hashlib.md5(request.form.get("ps1").encode())
            if ps.hexdigest() == ps1.hexdigest():
                Passwordupdate = Useruthentication.query.filter_by(mailid=g.user).first()
                print(Passwordupdate)
                Passwordupdate.userpassword = ps1.hexdigest()
                db.session.add(Passwordupdate)
                db.session.commit()
                flash("Password successfully change")
                return redirect(url_for('user'))
            else:
                flash("Password Doesnt Match", "danger")
                return redirect(url_for('Password_Update'))
        return render_template("pw.html")


@app.route('/userSignUp', methods=["POST"])
def UserSignUp():
    if request.method == 'POST':
        data = request.get_json()
        up = hashlib.md5(data['password'].encode())
        newUser = Useruthentication(username=data['username'],
                                    phno=data['phoneno'],
                                    mailid=data['email'],
                                    userpassword=up.hexdigest(),
                                    rectym=datetime.now())
        db.session.add(newUser)
        db.session.commit()
        return jsonify({"message": "signup"}), 200


@app.route('/GetOtp', methods=['POST'])
def GetOtp():
    if request.method == 'POST':
        data = request.get_json()
        result = Useruthentication.query.filter_by(mailid=data['email']).first()
        if result is not None:
            session["user"] = data['email']
            msg = Message('OTP', sender='nreply760@gmail.com', recipients=[result.mailid])
            msg.body = f"Hello {result.username} a request has been recieved to change the password for your Account your secret otp is \n {str(otp)}"
            mail.send(msg)
            return jsonify({"message": "GetOtp"}), 200


@app.route('/OTP_validation', methods=['POST'])
def OTP_validation():
    if g.user:
        if request.method == "POST":
            data = request.get_json()
            if data['otp'] == str(otp):
                return jsonify({"message": "otp"}), 200


@app.route('/Reset_Password', methods=['POST'])
def Reset_Password():
    if g.user:
        if request.method == "POST":
            data = request.get_json()
            ps = hashlib.md5(data['password'].encode())
            ps2 = hashlib.md5(data['password2'].encode())
            if ps.hexdigest() == ps2.hexdigest():
                Passwordupdate = Useruthentication.query.filter_by(mailid=g.user).first()
                Passwordupdate.userpassword = ps2.hexdigest()
                db.session.add(Passwordupdate)
                db.session.commit()
                return jsonify({"message": 'Reset_Password'}), 200


# Created an temporary app route to display the WeatherData which get accessed from the weather table
@app.route('/weather', methods=['GET'])
def getWeatherData():
    return render_template("weather.html", wdata=WeatherData.query.all())


@app.before_request
def before_request():
    g.user = None
    if "user" in session:
        g.user = session["user"]


if __name__ == "__main__":
    app.run(debug=True, port=5000)
