from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_login import LoginManager
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

from website import routes