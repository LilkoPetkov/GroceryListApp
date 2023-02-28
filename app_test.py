from flask import Flask
from flask_mail import Mail, Message

app = Flask(__name__)
mail= Mail(app)

app.config['MAIL_SERVER'] = 'mail.sportcentre.info'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'info@sportcentre.info'
app.config['MAIL_PASSWORD'] = '4|*1~@_^c131'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

@app.route("/")
def index():
   msg = Message('Hello', sender = 'info@sportcentre.info', recipients = ['lilko.petkovv@gmail.com'])
   msg.body = "Hello Flask message sent from Flask-Mail"
   mail.send(msg)
   return "Sent"

if __name__ == '__main__':
   app.run(debug = True)