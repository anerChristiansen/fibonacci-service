import os
from flask import Flask


__version__ = '0.0.1'


def create_app():
    # create flask app
    app = Flask(
                __name__,
                )

    # append version
    app.version = __version__

    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

    app.config['BLACKLIST'] = set()

    # # register api blueprints
    from project.server.api.routes import main_blueprint as api_blueprint
    app.register_blueprint(api_blueprint)

    return app