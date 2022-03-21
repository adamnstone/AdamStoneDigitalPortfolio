import os
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from wtforms import validators
from python_backend.constants import PYTHON_BACKEND_FOLDER
from python_backend.python_backend_main import sift_cards, compile_cards, create_id_lst, create_id_dict, add_card_to_document, TEMPORARY_SEND_DOWNLOAD_FILES_FOLDER
from python_backend.send_mail import send_mail
from flask import Flask, flash, request, render_template, send_from_directory, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Email, InputRequired, Length, ValidationError, Email, EqualTo
from flask_bcrypt import Bcrypt
from docx import Document
import os

# TODO find the most common cards
# TODO from url note school, student, side, and tournament

SEARCH_MESSAGE = "Search Cards"

QUERY_KEY = 'query'

app = Flask(__name__)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"
app.config['SECRET_KEY'] = 'kjw,ehn5fret4T#$#^$%^%^*^&4ggg'

MAIL_USER = "cardcollectordonotreply@gmail.com"
MAIL_PASS = "CARDCOLLECTORprogram1!##"

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)

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

@app.route("/", methods=['GET', 'POST'])
def home():
    return render_template("home.html")

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
        new_user = User(username=form.username.data, email=form.email.data, password=hashed_password)
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
        send_mail(MAIL_USER, 
            MAIL_PASS, 
            "Password Reset Request",
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

compiled_cards = []
card_database_dict = {}
case_database_lst = {}

def add_temporary_send_file_path(filename):
    return f"{PYTHON_BACKEND_FOLDER}/{TEMPORARY_SEND_DOWNLOAD_FILES_FOLDER}/{filename}"

def temporary_send_download_files_folder():
    return f"{PYTHON_BACKEND_FOLDER}/{TEMPORARY_SEND_DOWNLOAD_FILES_FOLDER}"

def create_send_download_folder():
    try:
        os.makedirs(temporary_send_download_files_folder())
    except FileExistsError:
        print(f"Skipping Creating Folder \"{temporary_send_download_files_folder()}\" -- already exists")

def send_download(filename):
    return send_from_directory(temporary_send_download_files_folder(), path=filename, as_attachment=True)

def update_cards():
    global card_database_dict, card_database_lst
    compiled_cards = compile_cards(download=True, download_delay=2, download_all_versions=False)
    card_database_dict = create_id_dict(compiled_cards) # {id: <card_object>}
    card_database_lst = create_id_lst(compiled_cards) # (id, <card_object>)

@app.route("/dashboard", methods=['GET', 'POST'])
@login_required
def dashboard():
    args = request.args
    if QUERY_KEY in args:
        query = args[QUERY_KEY]
        sifted_cards = sift_cards(query, True, cards=card_database_lst) # (id, (score, <card_object>))
        return render_template("dashboard.html", username=current_user.username, placeholder=query, cards=sifted_cards, query=query, has_query=True)
    else:
        return render_template("dashboard.html", username=current_user.username, placeholder=SEARCH_MESSAGE, has_query=False)

@app.route("/cards/<card_id>", methods=['GET', 'POST'])
@login_required
def card(card_id):
    card_id = int(card_id)
    args = request.args
    return render_template("card.html", card=card_database_dict[card_id], id=card_id, query=(args[QUERY_KEY] if QUERY_KEY in args else ""))

@app.route("/download/<card_id>", methods=['GET', 'POST'])
@login_required
def download(card_id):
    card_id = int(card_id)
    card = card_database_dict[card_id]
    document = Document()
    add_card_to_document(card, document)
    document.save(add_temporary_send_file_path(card.formatted_tag_as_filename))
    return send_download(card.formatted_tag_as_filename)

if __name__ == "__main__":
    create_send_download_folder()
    update_cards()
    app.run(host="0.0.0.0", port=80) # TODO update cards and clear the temporary downloads folder