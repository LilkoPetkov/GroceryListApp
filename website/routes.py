from werkzeug.security import generate_password_hash, check_password_hash
from flask import flash, render_template, request, redirect, url_for
from flask_mail import Message
from flask_login import login_user, logout_user, login_required, current_user
from website import app, db, mail
from website.models import Items, User


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

        elif request.form["submit_button"] == "Email":
            return redirect(url_for("send_email_page"))

        elif request.form["submit_button"] == "Logout":
            logout_user()

            flash("You have been logged out.", category="info")

            return redirect(url_for("index"))

        db.session.commit()

    return render_template("index.html", user=current_user)


@app.route("/send-email", methods=["POST", "GET"])
def send_email_page():
    if request.method == 'POST':
        if request.form['submit_button'] == 'Back':
            return redirect(url_for("index"))
        else:
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
