from rate import Rater, rate_link
from send_mail import send_mail
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import Flask, flash, request, render_template, send_from_directory, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, InputRequired, Length, ValidationError, Email, EqualTo
from flask_bcrypt import Bcrypt
from mutable_dict import MutableDict, JSONEncodedDict
import copy

CONTACT_EMAIL = "adam.stone.n@gmail.com"

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"
app.config['SECRET_KEY'] = 'kjw,ehn5fret4T#$#^$%^%^*^&4ggg'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

CHILD_TO_PARENT_EMAILS = {} # {child_email: parent_email}

# database children -- {child_name: (settings, child_emails)}

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)
    children = db.Column(MutableDict.as_mutable(JSONEncodedDict))

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    @staticmethod
    def get_child_google_account_token(child_google_account, parent_email, child_name, expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({"child_google_account": child_google_account, "parent_email": parent_email, "child_name": child_name}).decode("utf-8")

    @staticmethod
    def verify_child_google_account_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return None
        return data

def load_child_to_parent_emails():
    for u in User.query.filter_by():
        children_settings = u.children
        for child_name in children_settings:
            for child_email in children_settings[child_name][1]:
                CHILD_TO_PARENT_EMAILS[child_email] = u.email

# RATING #

rater = Rater()

def get_child_settings_from_email(child_email, children_settings):
    for name in children_settings:
        if child_email in children_settings[name][1]:
            return children_settings[name][0]
    return None

@app.route("/get_settings", methods=['POST'])
def get_settings():
    req_data = request.json
    email = req_data['email']
    if email not in CHILD_TO_PARENT_EMAILS:
        return {"status": "error", "message": f"'{email}' not affiliated with any account"}
    parent_email = CHILD_TO_PARENT_EMAILS[email]
    children_settings = User.query.filter_by(email=parent_email).first().children
    settings = {**get_child_settings_from_email(email, children_settings), "toEmail": parent_email}  # TODO toEmail wasn't there this is a patch
    return {"status": "success", "settings": settings}

@app.route("/get_child_settings", methods=['POST'])
@login_required
def get_child_settings():
    req_data = request.json
    child_name = req_data['childName']
    return {"status": "success", "settings": current_user.children[child_name][0]}

@app.route("/update_settings", methods=['POST'])
@login_required
def update_settings():
    req_data = request.json
    old_settings = current_user.children
    new_settings = req_data['new_settings']
    current_user.children = new_settings
    db.session.commit()
    for child_name in old_settings:
        for child_email in old_settings[child_name][1]:
            CHILD_TO_PARENT_EMAILS.pop(child_email)
    for child_name in new_settings:
        for child_email in new_settings[child_name][1]:
            CHILD_TO_PARENT_EMAILS[child_email] = current_user.email
    return {"status": "success"}

@app.route("/modify_child_settings", methods=['POST'])
@login_required
def modify_child_settings():
    req_data = request.json
    child_name = req_data['childName']
    if child_name not in current_user.children:
        return {"status": "error", "message": f"Child '{child_name} Does Not Exist"}
    current_user.children[child_name] = [req_data['new_settings'], current_user.children[child_name][1]]
    db.session.commit()
    return {"status":"success"}

@app.route("/add_child", methods=['POST'])
@login_required
def add_child():
    req_data = request.json
    child_name = req_data['name']
    child_settings = req_data['settings']
    child_google_accounts = req_data['emails']
    if child_name in current_user.children:
        return {"status": "error", "message": "Child Already Exists"}
    current_user.children = {child_name: [child_settings, child_google_accounts], **current_user.children}
    db.session.commit()
    for email in child_google_accounts:
        CHILD_TO_PARENT_EMAILS[email] = current_user.email
    return {"status": "success"}

@app.route("/add_child_account_email", methods=['POST'])
@login_required
def add_child_account_email():
    req_data = request.json
    child_email = req_data['email']
    child_name = req_data['childName']
    token = User.get_child_google_account_token(child_email, current_user.email, child_name)
    send_mail("Password Reset Request",
            f"To add a google account to the child, visit the following link:\n{url_for('add_child_token', token=token, _external=True)}\n\nIf you did not make this request, simply ignore this email and no changes will be made.", 
            child_email)
    CHILD_TO_PARENT_EMAILS[child_email] = current_user.email
    return {"status": "success"}

@app.route("/delete_child", methods=['POST'])
@login_required
def delete_child():
    req_data = request.json
    child_name = req_data['childName']
    if child_name not in current_user.children:
        return {"status": "error", "message": "Child Does Not Exist"}
    current_user.children.pop(child_name)
    db.session.commit()
    return {"status": "success"}

@app.route("/delete_google_account", methods=['POST'])
@login_required
def delete_google_account():
    req_data = request.json
    child_name = req_data['childName']
    child_google_account = req_data['account']
    accs = copy.copy(current_user.children[child_name])
    accs[1].remove(child_google_account)
    current_user.children[child_name] = accs
    db.session.commit()
    print(current_user.children)
    return {"status": "success"}

@app.route("/rate", methods=['POST'])
def rate_route():
    req_data = request.json
    link = req_data['link']
    block_report_no_transcript = req_data['block_report_no_transcript']
    has_transcript = True
    data = None
    data = rate_link(link, rater=rater)
    if not data:
        if not block_report_no_transcript:
            return {"status": "success", "transcript": False}
        has_transcript = False
    if has_transcript:
        level, word, stats = data
    to_email = req_data['email']
    block_video = req_data['block_video']
    report_level = int(req_data['report_level'])
    date_time = req_data['date_time']
    if has_transcript:
        if level >= report_level:
            send_mail(f"YouTube Rater: {word}", f"{link} with a rating of {word} contained the words {stats} and was watched {date_time}." + ("\n\nThis video was blocked." if block_video else ""), to_email)
    else:
        send_mail("YouTube Rater: No Transcript", f"{link} had no transcript available." + ("\n\nThis video was blocked." if block_video else ""), to_email)
    return {"status": "success", "transcript": has_transcript, "level": (level if has_transcript else None)}

# ACCOUNTS #

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class RegisterForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(
        min=4, max=20)], render_kw={"placeholder": "Username"})

    email = StringField(validators=[InputRequired(), Email()], 
        render_kw={"placeholder": "Email"})

    password = PasswordField(validators=[InputRequired(), Length(
        min=4, max=20)], render_kw={"placeholder": "Password"})

    confirm_password = PasswordField(validators=[InputRequired(), EqualTo("password", message="\"Password\" and \"Confirm Password\" fields do not match.")],
        render_kw={"placeholder": "Confirm Password"})

    submit = SubmitField("Register")

    def validate_username(self, username):
        existing_user_username = User.query.filter_by(
            username=username.data).first()

        if existing_user_username:
            raise ValidationError(
                "That username already exists. Please choose a different one.")

class LoginForm(FlaskForm):
    email = StringField(validators=[InputRequired(), Email()], 
    render_kw={"placeholder": "Email"})

    password = PasswordField(validators=[InputRequired(), Length(
        min=4, max=20)], render_kw={"placeholder": "Password"})

    submit = SubmitField("Login")

class RequestResetForm(FlaskForm):
    email = StringField(validators=[InputRequired(), Email()], 
    render_kw={"placeholder": "Email"})

    submit = SubmitField("Request Password Reset")

    def valdate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError("There is no account associated with that email. You must register first.")

class ResetPasswordForm(FlaskForm):
    password = PasswordField(validators=[InputRequired(), Length(
        min=4, max=20)], render_kw={"placeholder": "Password"})
    
    confirm_password = PasswordField(validators=[InputRequired(), EqualTo("password")],
        render_kw={"placeholder": "Confirm Password"})

    submit = SubmitField("Reset Password")

    def validate_username(self, username):
        existing_user_username = User.query.filter_by(
            username=username.data).first()

        if existing_user_username:
            raise ValidationError(
                "That username already exists. Please choose a different one.")

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('dashboard'))
    return render_template("login.html", form=form)

@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        new_user = User(username=form.username.data, email=form.email.data, password=hashed_password, children={})
        db.session.add(new_user)
        try:
            db.session.commit()
        except:
            flash("An account has already been created with this username and/or email.")
            return redirect(url_for("register"))
        return redirect(url_for("login"))
    
    return render_template("register.html", form=form)

@app.route("/reset_password", methods=['GET', 'POST'])
def reset_password():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard"))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        token = user.get_reset_token()
        send_mail("Password Reset Request",
            f"To reset your password, visit the following link:\n{url_for('reset_token', token=token, _external=True)}\n\nIf you did not make this request, simply ignore this email and no changes will be made.", 
            user.email)
        flash("An email has been sent with instructions to reset your password. If you do not see it, try checking your spam.")
        return redirect(url_for("login"))
    return render_template("reset_request.html", form=form)

@app.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    user = User.verify_reset_token(token)
    if user is None:
        flash("That is an invalid or expired token", "warning")  # ALERT?
        return redirect(url_for("reset_request"))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        user.password = hashed_password
        db.session.commit()
        return redirect(url_for("login"))
    return render_template("reset_token.html", form=form)

# MAIN #

@app.route("/", methods=['GET'])
def home():
    return render_template("home.html")

@app.route("/dashboard", methods=['GET'])
@login_required
def dashboard():
    all_children_settings = current_user.children
    return render_template("dashboard.html", username=current_user.username, parent_email=current_user.email, all_children_settings=all_children_settings)

@app.route("/child_settings/<child_name>", methods=['GET'])
@login_required
def new_child(child_name):
    if child_name not in current_user.children:
        return {"status": "error", "message": f"Child '{child_name}' Does Not Exist"}
    print(current_user.children)
    child_info = current_user.children[child_name]
    child_google_accounts = child_info[1]
    child_settings = child_info[0]
    return render_template("child_settings.html", child_name=child_name, parentEmail=current_user.email, child_google_accounts={"accounts": child_google_accounts}, child_settings = child_settings)  # as dict with list so that jinja passing is easier

@app.route("/add_child_token/<token>", methods=['GET'])
def add_child_token(token):
    data = User.verify_child_google_account_token(token)
    if data is None:
        return render_template("error.html", message="That is an invalid or expired token")
    parent_email = data['parent_email']
    child_email = data['child_google_account']
    child_name = data['child_name']
    u = User.query.filter_by(email=parent_email).first()
    if u is None:
        return {"status": "error", "message": "Parent Email Does Not Exist"}
    u.children[child_name] = [u.children[child_name][0], [*u.children[child_name][1], child_email]]
    db.session.commit()
    return render_template("success.html", 
        message=f"Google account added successfully! Return to {parent_email}'s account or return to login.", 
        has_link=True, 
        link="Click here to login", 
        href=url_for('login'))

@app.route("/contact", methods=['POST'])
def contact():
    req_data = request.json
    name, email, message = req_data['name'], req_data['email'], req_data['message']
    send_mail('Client Contact', f"Name: {name}\nEmail: {email}\nMessage: {message}", CONTACT_EMAIL)
    return {"status": "success"}

if __name__ == "__main__":
    load_child_to_parent_emails()
    app.run(host="0.0.0.0", port=80)