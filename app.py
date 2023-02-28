import flask_login
from flask import Flask, flash, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
from flask_login import UserMixin, login_user, logout_user, login_required, LoginManager

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///grocery.db"
app.config["SECRET_KEY"] = "30f6735b3cd39d20a9d7276e"

db = SQLAlchemy(app)

app.config['MAIL_SERVER'] = 'mail.sportcentre.info'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'info@sportcentre.info'
app.config['MAIL_PASSWORD'] = '4|*1~@_^c131'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)
login_manager = LoginManager(app)
login_manager.login_view = "login_page"
login_manager.login_message_category = "info"


class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=30), nullable=False, unique=True)
    password = db.Column(db.String(length=60), nullable=False)
    items = db.relationship("Items", backref='owned_user', lazy="dynamic")


class Items(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(length=30), nullable=False)
    number = db.Column(db.Integer, nullable=False)
    owner = db.Column(db.Integer(), db.ForeignKey("user.id"))


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
            item_to_add = Items(name=request.form.get("name"), number=request.form.get("number"))


            """
            i1 = Item.query.filter_by(name="Butter").first()
            u1 = User.query.filter_by(username="lilko").first()
            
            i1.owner = u1.id
            db.session.add(i1)
            db.session.commit()
            """

            db.session.add(item_to_add)

        elif request.form["submit_button"] == "Proceed":
            return redirect(url_for("send_email_page"))

        elif request.form["submit_button"] == "Logout":
            logout_user()

            flash("You have been logged out.", category="info")

            return redirect(url_for("index"))

        db.session.commit()

    current_items = Items.query.all()

    return render_template("index.html", current_items=current_items)


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
    password = request.form.get("password")

    if username and password:
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
            if current_user.password == password:
                login_user(current_user)
                flash("Success! You are logged in!", category="success")

                return redirect(url_for("index"))
            else:
                flash("Username or password does not match. Please provide a valid one.", category="danger")
        else:
            flash("Username and password do not match. Please register an account.", category="danger")

    return render_template("login.html")


if __name__ == "__main__":
    app.run(debug=True)
