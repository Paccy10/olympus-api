""" Module for sending emails """

from smtplib import SMTPException
from flask import render_template
from flask_mail import Message

from config.server import mail
from .tokens_handler import generate_user_token


def send_email(user, subject, template):
    """ Sends Email """

    try:
        token = generate_user_token(user['id'])
        message = Message(subject, sender=(
            'Olympus', 'authors.heaven2020@gmail.com'), recipients=[user['email']])
        message.html = render_template(template, user=user, token=token)

        mail.send(message)
        return True

    except SMTPException:
        return False
