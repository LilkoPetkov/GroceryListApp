import smtplib

def send_mail():
    mail = 'lilko.petkovv@gmail.com'

    user = 'info@sportcentre.info'
    gmail_password = '4|*1~@_^c131'

    sent_from = user
    to = [mail]
    subject = f'Grocery List'
    body = "Test this message"

    email_text = """\
    From: %s
    To: %s
    Subject: %s
    %s
    """ % (sent_from, to, subject, body)

    try:
        smtp_server = smtplib.SMTP_SSL('mail.sportcentre.info', 465)
        smtp_server.ehlo()
        smtp_server.login(user, gmail_password)
        smtp_server.sendmail(sent_from, to, email_text)
        smtp_server.close()
        print("Email sent successfully!")
    except Exception as ex:
        print("Something went wrong….",ex)


print(send_mail())
