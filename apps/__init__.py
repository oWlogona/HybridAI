from flask import Flask
from flask_wtf.csrf import CSRFProtect

from apps.polls.views import poll
from config import config_dict
from utils import db


def create_app(config=config_dict['dev']):
    app = Flask(__name__, template_folder='../templates')
    app.config.from_object(config_dict['dev'])
    csrf = CSRFProtect(app)
    csrf.init_app(app)
    db.init_app(app)

    app.register_blueprint(poll)

    @app.shell_context_processor
    def make_shell_context():
        return {
            'db': db,
        }

    return app
