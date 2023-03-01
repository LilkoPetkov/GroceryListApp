from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, flash, render_template, request, redirect, url_for, g
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
from flask_login import UserMixin, login_user, logout_user, login_required, LoginManager, current_user
from flask_migrate import Migrate
from decouple import config


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{config("DB_USER")}:{config("DB_PASSWORD")}' \
                                              f'@localhost:{config("DB_PORT")}/{config("DB_NAME")}'
app.config["SECRET_KEY"] = "30f6735b3cd39d20a9d7276e"

db = SQLAlchemy(app)
migrate = Migrate(app, db)

app.config['MAIL_SERVER'] = config("MAIL_SERVER")
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = config("MAIL_USERNAME")
app.config['MAIL_PASSWORD'] = config("MAIL_PASSWORD")
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)
login_manager = LoginManager(app)
login_manager.login_view = "login_page"
login_manager.login_message_category = "info"


class Items(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(length=70), nullable=False)
    number = db.Column(db.Integer, nullable=False)
    owner = db.Column(db.Integer, db.ForeignKey("user.id"))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(length=30), nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    items = db.relationship("Items", backref='owned_user', lazy="dynamic")


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route("/", methods=["GET", "POST"])
@app.route("/home", methods=["GET", "POST"])
@login_required
def index():
    if request.method == 'POST':
        if request.form['submit_button'] == 'Clear':
            Items.query.delete()

        elif request.form["submit_button"] == "Add":
            item_to_add = Items(name=request.form.get("name"), number=request.form.get("number"), owner=current_user.id)

            db.session.add(item_to_add)

        elif request.form["submit_button"] == "Proceed":
            return redirect(url_for("send_email_page"))

        elif request.form["submit_button"] == "Logout":
            logout_user()

            flash("You have been logged out.", category="info")

            return redirect(url_for("index"))

        db.session.commit()

    return render_template("index.html", user=current_user)


@app.route("/send-email", methods=["POST", "GET"])
def send_email_page():
    email = request.form.get("email")
    items = ["Item List: "]

    for item in Items.query.all():
        items.append(f"{item.name} - {item.number}")

    if email:
        msg = Message('Grocery List', sender='info@sportcentre.info', recipients=[email])
        msg.body = '\n'.join(items)
        mail.send(msg)
        flash("Email sent successfully.", category="success")

    return render_template("email.html")


@app.route("/register", methods=["GET", "POST"])
def register_page():
    username = request.form.get("username")
    passw = request.form.get("password")

    if username and passw:
        password = generate_password_hash(passw, method='sha256')

        user_to_create = User(username=username, password=password)

        db.session.add(user_to_create)
        db.session.commit()

        return redirect(url_for("index"))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login_page():
    username = request.form.get("username")
    password = request.form.get("password")

    current_user = User.query.filter_by(username=username).first()

    if request.method == 'POST':
        if current_user:
            if check_password_hash(current_user.password, password):
                login_user(current_user, remember=True)
                flash("Success! You are logged in!", category="success")

                return redirect(url_for("index"))
            else:
                flash("Username or password does not match. Please provide a valid one.", category="danger")
        else:
            flash("Username and password do not match. Please register an account.", category="danger")

    return render_template("login.html")


if __name__ == "__main__":
    app.run(debug=True)
