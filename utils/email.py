import os
from threading import Thread

from flask import Flask
from flask_mail import Mail, Message


class MailFactory(Mail):
    app: Flask = None

    def __init__(self, app: Flask = None):
        app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
        app.config['MAIL_PORT'] = os.getenv('MAIL_PORT')
        app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
        app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
        app.config['MAIL_USE_TLS'] = False
        app.config['MAIL_USE_SSL'] = True

        self.app = app

        super().__init__(app)

    def init_app(self, app: Flask) -> None:
        self.app = app
        super().init_app(app)

    def send_message_async(self, *args, **kwargs) -> Thread:
        msg = Message(*args, **kwargs)

        thread = Thread(target=self.send, args=[msg])
        thread.start()
        return thread
