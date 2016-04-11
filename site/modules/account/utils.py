import random
import smtplib
import string

from app import app
from email.mime.text import MIMEText
from flask import url_for

valid_chars = string.ascii_letters + string.digits
confirm_email_template = """Hi {first_name},
Thanks for signing up for {application}. Please click the following
link (or copy and paste it into your browser) in order to verify your email:

{confirm_email_link}

If you did not create an account on {application}, please ignore this email."""

def generate_confirmation_key():
    return "".join([random.choice(valid_chars) for i in range(64)])

def send_confirm_email(first_name, email):
    if not app.config['SEND_EMAIL']:
        return None

    confirm_key = generate_confirmation_key()
    confirm_email_link = url_for('account.confirm_email', key=confirm_key, _absolute=True)
    message = MIMEText(confirm_email_template.format(first_name=first_name,
                                                     application=app.config['APP_NAME'],
                                                     confirm_email_link=confirm_email_link))
    message['Subject'] = "Please confirm your {} account".format(app.config['APP_NAME'])
    message['From'] = app.config['EMAIL_FROM']
    message['To'] = email

    smtp = smtplib.SMTP('localhost')
    smtp.sendmail(message)
    smtp.quit()

    return confirm_key
