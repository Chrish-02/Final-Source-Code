from flask_wtf import FlaskForm
from wtforms import StringField,HiddenField,DecimalField,PasswordField, SubmitField, TextAreaField, DateField, SelectField,BooleanField,IntegerField,FileField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from application.models import User, Admin,Createemp,Leaveapply,Resign

class LoginForm(FlaskForm):
    username   = StringField("Username", validators=[DataRequired(), Length(min=6,max=15)])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6,max=15)])
    remember_me = BooleanField("Remember Me")
    submit = SubmitField("Login")

class RegisterForm(FlaskForm):
    username=StringField("Username", validators=[DataRequired(),Length(min=6,max=15)])
    password = PasswordField("Password", validators=[DataRequired(),Length(min=6,max=15)])
    password_confirm = PasswordField("Confirm Password", validators=[DataRequired(),Length(min=6,max=15), EqualTo('password')])
    submit = SubmitField("Register")

class CreateempForm(FlaskForm):
    id = HiddenField()
    firstname = StringField("First Name*",validators=[DataRequired(),Length(min=1,max=100)])
    lastname = StringField("Last Name*",validators=[DataRequired(),Length(min=1,max=100)])
    age= IntegerField("Age*",validators=[DataRequired()])
    gender = SelectField("Gender*", choices=[('Male', 'Male'), ('Female', 'Female')])
    address = TextAreaField("Address*", validators=[DataRequired()])
    email = StringField("Email Id*", validators=[Email()])
    designation =  StringField("Designation*",validators=[DataRequired(),Length(min=1,max=100)])
    department =  StringField("Department*",validators=[DataRequired(),Length(min=1,max=100)])
    basic=DecimalField("Basic Pay*")
    pf=DecimalField("Provident Fund*")
    mf=DecimalField("Medical*")
    submit = SubmitField("Save")
    
class LeaveapplyForm(FlaskForm):
    id = HiddenField()
    email = StringField("Email Id*", validators=[Email()])
    firstname = StringField("First Name*",validators=[DataRequired(),Length(min=1,max=100)])
    lastname = StringField("Last Name*",validators=[DataRequired(),Length(min=1,max=100)])
    startdate = DateField("Start Date*", validators=[DataRequired()],format='%Y-%m-%d')
    enddate= DateField("End Date*",validators=[DataRequired()],format='%Y-%m-%d')
    cause = TextAreaField("Cause of Leave*", validators=[DataRequired()])
    status =HiddenField()
    submit = SubmitField("Apply")

class ResignForm(FlaskForm):
    id = HiddenField()
    firstname = StringField("First Name*",validators=[DataRequired(),Length(min=1,max=100)])
    lastname = StringField("Last Name*",validators=[DataRequired(),Length(min=1,max=100)])
    email = StringField("Email Id*", validators=[Email()])
    jdate = DateField("Joining Date*", validators=[DataRequired()],format='%Y-%m-%d')
    resigndate= DateField("Resign Date*",validators=[DataRequired()],format='%Y-%m-%d')
    cause = TextAreaField("Cause of Resign*", validators=[DataRequired()])
    submit = SubmitField("Submit")

class PayrollForm(FlaskForm):
    id = HiddenField()
    name = StringField("Name*",validators=[DataRequired(),Length(min=1,max=100)])
    email = StringField("Email Id*", validators=[Email()])
    department= StringField("Department*",validators=[DataRequired(),Length(min=1,max=100)])
    shift = SelectField("Shift*", choices=[('Morning', 'Morning'), ('Day', 'Day'), ('Night', 'Night')])
    fdate = DateField("From*", validators=[DataRequired()],format='%Y-%m-%d')
    tdate= DateField("To*",validators=[DataRequired()],format='%Y-%m-%d')
    sdate= DateField("Salary Date*",validators=[DataRequired()],format='%Y-%m-%d')
    gross=DecimalField("Gross Salary*")
    final=DecimalField("Final Salary*")
    status =HiddenField()
    submit = SubmitField("Save")

class HolidayForm(FlaskForm):
    id = HiddenField()
    month = SelectField("Month", choices=[('January', 'January'), ('February', 'February'), ('March', 'March'),('April', 'April'), ('May', 'May'), ('June', 'June'),('July', 'July'), ('August', 'August'), ('September', 'September'),('October', 'October'), ('November', 'November'), ('December', 'December')])
    edate = DateField("Date", validators=[DataRequired()],format='%Y-%m-%d')
    event= StringField("Event",validators=[DataRequired(),Length(min=1,max=100)])
    submit = SubmitField("Add")
