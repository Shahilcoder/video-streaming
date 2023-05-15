from flask import Flask
from flask_cors import CORS


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping()
    CORS(app)

    @app.route("/")
    def index():
        return "Python server"

    from api import api
    app.register_blueprint(api)

    return app
