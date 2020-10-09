import flask
from application import db
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(64), nullable=True)

class Admin(UserMixin,db.Model):
    __tablename__ = 'admins'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), nullable=False)
    password = db.Column(db.String(64), nullable=False)

class Createemp(UserMixin, db.Model):
    __tablename__ = 'employees'
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(64), nullable=False)
    lastname = db.Column(db.String(64), nullable=False)
    age = db.Column(db.Numeric(64), nullable=False)
    gender = db.Column(db.String(64), nullable=False)
    # bdate = db.Column(db.String(64), nullable=False)
    # jdate = db.Column(db.String(64), nullable=False)
    address = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(64), nullable=True)
    designation= db.Column(db.String(64), nullable=False)
    department= db.Column(db.String(64), nullable=False)
    basic = db.Column(db.Numeric(64), nullable=False)
    pf = db.Column(db.Numeric(64), nullable=False)
    mf = db.Column(db.Numeric(64), nullable=False)

class Leaveapply(UserMixin, db.Model):
    __tablename__ = 'leaveapply'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), nullable=False)
    firstname = db.Column(db.String(64), nullable=False)
    lastname = db.Column(db.String(64), nullable=False)
    startdate = db.Column(db.String(64), nullable=False)
    enddate = db.Column(db.String(64), nullable=False)
    cause = db.Column(db.String(64), nullable=False)
    status=db.Column(db.String(64), default='Pending')

class Resign(UserMixin, db.Model):
    __tablename__ = 'resignform'
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(64), nullable=False)
    lastname = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(64), nullable=False)
    jdate = db.Column(db.String(64), nullable=False)
    resigndate = db.Column(db.String(64), nullable=False)
    cause=db.Column(db.String(64), nullable=False)

class Payroll(UserMixin, db.Model):
    __tablename__ = 'payroll'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(64), nullable=True)
    department= db.Column(db.String(64), nullable=False)
    shift = db.Column(db.String(64), nullable=False)
    fdate = db.Column(db.String(64), nullable=False)
    tdate = db.Column(db.String(64), nullable=False)
    sdate = db.Column(db.String(64), nullable=False)
    gross = db.Column(db.Numeric(64), nullable=False)
    final = db.Column(db.Numeric(64), nullable=False)
    status=db.Column(db.String(64), default='Paid')

class Holiday(UserMixin, db.Model):
    __tablename__ = 'holiday'
    id = db.Column(db.Integer, primary_key=True)
    month=db.Column(db.String(64), nullable=False)
    edate=db.Column(db.String(64), nullable=False)
    event=db.Column(db.String(64), nullable=False)

