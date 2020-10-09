from application import app, db
from flask import flash,render_template, request, json, Response,url_for, current_app, redirect, flash,session
from rauth import OAuth2Service
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user, login_required
import json
import urllib.request as urllib2
from application.forms import LoginForm, RegisterForm,CreateempForm,LeaveapplyForm,ResignForm,PayrollForm,HolidayForm
from application.models import User, Admin,Createemp, Leaveapply,Resign,Payroll,Holiday

class OAuthSignIn(object):
    providers = None

    def __init__(self, provider_name):
        self.provider_name = provider_name
        credentials = current_app.config['OAUTH_CREDENTIALS'][provider_name]
        self.consumer_id = credentials['id']
        self.consumer_secret = credentials['secret']

    def authorize(self):
        pass

    def callback(self):
        pass

    def get_callback_url(self):
        return url_for('oauth_callback', provider=self.provider_name,
                        _external=True)

    @classmethod
    def get_provider(self, provider_name):
        if self.providers is None:
            self.providers={}
            for provider_class in self.__subclasses__():
                provider = provider_class()
                self.providers[provider.provider_name] = provider
        return self.providers[provider_name]

class GoogleSignIn(OAuthSignIn):
    def __init__(self):
        super(GoogleSignIn, self).__init__('google')
        googleinfo = urllib2.urlopen('https://accounts.google.com/.well-known/openid-configuration')
        google_params = json.load(googleinfo)
        self.service = OAuth2Service(
                name='google',
                client_id=self.consumer_id,
                client_secret=self.consumer_secret,
                authorize_url=google_params.get('authorization_endpoint'),
                base_url=google_params.get('userinfo_endpoint'),
                access_token_url=google_params.get('token_endpoint')
        )

    def authorize(self):
        return redirect(self.service.get_authorize_url(
            scope='email',
            response_type='code',
            redirect_uri=self.get_callback_url())
            )

    def callback(self):
        if 'code' not in request.args:
            return None, None, None
        oauth_session = self.service.get_auth_session(
                data={'code': request.args['code'],
                      'grant_type': 'authorization_code',
                      'redirect_uri': self.get_callback_url()
                     },
                decoder = json.loads
        )
        me = oauth_session.get('').json()
        return me['email']

lm = LoginManager(app)
lm.init_app(app)

lm.login_view = 'index'

@lm.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/emplayout')
def emplayout():
    return render_template('emplayout.html')

@app.route('/adminlayout')
def adminlayout():
    return render_template('adminlayout.html')

@app.route('/authorize/<provider>')
def oauth_authorize(provider):
    # Flask-Login function
    if not current_user.is_anonymous:
        return redirect(url_for('emplayout'))
    oauth = OAuthSignIn.get_provider(provider)
    return oauth.authorize()

@app.route('/callback/<provider>')
def oauth_callback(provider):
    if not current_user.is_anonymous:
        return redirect(url_for('emplayout'))
    oauth = OAuthSignIn.get_provider(provider)
    email = oauth.callback()
    if email is None:
        # I need a valid email address for my user identification
        flash('Authentication failed.')
        return redirect(url_for('index'))
    #Look if the user already exists
    user=User.query.filter_by(email=email).first()
    if not user:
        # Create the user. Try and use their name returned by Google,
        # but if it is not set, split the email address at the @.
        nickname = None
        if nickname is None or nickname == "":
            nickname = email.split('@')[0]

        # We can do more work here to ensure a unique nickname, if you 
        # require that.
        user=User(nickname=nickname, email=email)
        db.session.add(user)
        db.session.commit()
    # Log in the user, by default remembering them for their next visit
    # unless they log out.
    login_user(user, remember=True)
    print(email)
    return redirect(url_for('emplayout'))

@app.route("/register", methods=['POST','GET'])
def register():
    if session.get('username'):
        return redirect(url_for('index'))
    form = RegisterForm()
    if form.validate_on_submit():
        username       = form.username.data
        password    = form.password.data

        admin = Admin(username=username,password=password)
        db.session.add(admin)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template("register.html", title="Register", form=form, register=True)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # check whether employee exists in the database and whether
        # the password entered matches the password in the database
        username    = form.username.data
        password    = form.password.data

        admin = Admin.query.filter_by(username=form.username.data).first()
        if admin and admin.password==password:
            login_user(admin)
            db.session.add(admin)
            db.session.commit()
            flash(f"{admin.username}, you are successfully logged in!", "success")
            return redirect(url_for('adminlayout'))
        else:
            flash('Invalid email or password!')
    return render_template('login.html', form=form, title='Login')

@app.route("/createemp", methods=["GET", "POST"])
def createemp():
    form = CreateempForm(request.form)
    employees = Createemp.query.all()
    if form.validate_on_submit():
        employee =Createemp(firstname=form.firstname.data,lastname=form.lastname.data,age=form.age.data,gender=form.gender.data,address=form.address.data,designation=form.designation.data,department=form.department.data,basic=form.basic.data, email=form.email.data, pf=form.pf.data,mf=form.mf.data)
        db.session.add(employee)
        db.session.commit()
        flash("Added Employee Successfully!")
        return redirect(url_for('adminlayout'))
    return render_template("createemp.html", title="Add Employee Details", form=form, employees=employees)

@app.route("/empdetails", methods=["GET","POST"])
def empdetails():
    rows=Createemp.query.all()
    return render_template ('empdetails.html', rows=rows)
    
@app.route('/updateemp/<id>/', methods=['GET', 'POST'])
def updateemp(id):
    employee =Createemp.query.get(id)
    form=CreateempForm(obj=employee)
    if form.validate_on_submit():
        form.populate_obj(employee)
        db.session.commit()
        return redirect(url_for('empdetails'))
    return render_template('updateemp.html',form=form,title="Update Employees")

@app.route('/deleteemp/<id>/', methods=['GET', 'POST'])
def deleteemp(id):
    Createemp.query.filter_by(id=id).delete()
    db.session.commit()
    return redirect(url_for('empdetails'))
    

@app.route("/leaveform", methods=["GET", "POST"])
def leaveform():
    form = LeaveapplyForm(request.form)
    leaveapplies = Leaveapply.query.all()
    if form.validate_on_submit():
        leaveapply =Leaveapply(email=form.email.data,firstname=form.firstname.data,lastname=form.lastname.data,startdate=form.startdate.data,enddate=form.enddate.data,cause=form.cause.data)
        db.session.add(leaveapply)
        db.session.commit()
        return redirect(url_for('checkleave'))
    return render_template("leaveform.html", title="Apply Leave", form=form, leaveapplies=leaveapplies)

@app.route("/resignform", methods=["GET", "POST"])
def resignform():
    form = ResignForm(request.form)
    resignapplies = Resign.query.all()
    if form.validate_on_submit():
        resign =Resign(firstname=form.firstname.data,lastname=form.lastname.data,email=form.email.data,jdate=form.jdate.data,resigndate=form.resigndate.data,cause=form.cause.data)
        db.session.add(resign)
        db.session.commit()
        flash("We will contact you shortly.")
        return redirect(url_for('emplayout'))
    return render_template("resignform.html", title="resign", form=form, resignapplies=resignapplies)

@app.route("/manageleave", methods=["GET","POST"])
def manageleave():
    rows=Leaveapply.query.all()
    return render_template ('manageleave.html', rows=rows)

@app.route("/checkleave", methods=["GET","POST"])
def checkleave():
    rows=Leaveapply.query.all()
    return render_template ('checkleave.html', rows=rows)

@app.route("/approveleave/<id>/", methods=["GET","POST"])
def approveleave(id):
    row=Leaveapply.query.get(id)
    row.status="Approved"
    db.session.commit()
    return redirect(url_for('manageleave'))
    
@app.route("/rejectleave/<id>/", methods=["GET","POST"])
def rejectleave(id):
    row=Leaveapply.query.get(id)
    row.status="Rejected"
    db.session.commit()
    return redirect(url_for('manageleave'))

@app.route("/holidaylistadmin", methods=["GET","POST"])
def holidaylistadmin():
    rows=Holiday.query.all()
    return render_template ('holidaylistadmin.html',rows=rows)

@app.route("/holidaylistemp", methods=["GET","POST"])
def holidaylistemp():
    rows=Holiday.query.all()
    return render_template ('holidaylistemp.html',rows=rows)

@app.route("/salaryform", methods=["GET", "POST"])
def salaryform():
    form = PayrollForm(request.form)
    pay= Payroll.query.all()
    if form.validate_on_submit():
        paying =Payroll(name=form.name.data,email=form.email.data,department=form.department.data,shift=form.shift.data,fdate=form.fdate.data,tdate=form.tdate.data,sdate=form.sdate.data,gross=form.gross.data,final=form.final.data)
        db.session.add(paying)
        db.session.commit()
        flash("Saved!")
        return redirect(url_for('adminlayout'))
    return render_template("salaryform.html", title="Payroll", form=form, pay=pay)

@app.route("/holidayentry", methods=["GET", "POST"])
def holidayentry():
    form = HolidayForm(request.form)
    holiday= Holiday.query.all()
    if form.validate_on_submit():
        holidays=Holiday(month=form.month.data,edate=form.edate.data,event=form.event.data)
        db.session.add(holidays)
        db.session.commit()
        return redirect(url_for('holidaylistadmin'))
    return render_template("holidayentry.html", title="Holiday", form=form, holiday=holiday)

@app.route("/salarystatus", methods=["GET","POST"])
def salarystatus():
    rows=Payroll.query.all()
    return render_template ('salarystatus.html', rows=rows)
