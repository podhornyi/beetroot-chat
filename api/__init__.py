from flask import Flask
import os
import json

from .db import init_db


class ChatApplication(Flask):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.config['SECRET_KEY'] = 'megasecret'

        self.debug = True
        self._register_error_handlers()

        self.config.update(
            self._get_external_config()
        )

        # self.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://chat:chat@chat_db/chat'
        # self.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////opt/app/db/chat.db'
        

    def _get_external_config(self) -> dict:
        if not os.environ.get('FLASK_CONFIG'):
            return dict()

        file_config_path = os.environ['FLASK_CONFIG']
        if not os.path.exists(file_config_path):
            return dict()

        with open(file_config_path) as f:
            return json.loads(f.read())

    def _register_error_handlers(self):

        def error_404(*args, **kwargs):
            return 'Oops 404', 404

        def error_403(*args, **kwargs):
            return 'Oops 403', 403

        def error_401(*args, **kwargs):
            return 'Oops 401', 401

        self.register_error_handler(401, error_401)
        self.register_error_handler(403, error_403)
        self.register_error_handler(404, error_404)


def create_app():
    app = ChatApplication('ChatApplication', template_folder='/opt/app/api/templates')

    print(app.url_map)
    init_db(app)

    from api.db.storage import Storage
    from .db import db

    app.storage = Storage()

    from .routes import register_views
    register_views(app)

    return app
