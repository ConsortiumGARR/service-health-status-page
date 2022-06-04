import os
from flask import Flask
from flask_cors import CORS
from .error_handler import init_errorhandler
from .flask_influxdb import FlaskInfluxDB

InfluxDB = FlaskInfluxDB()


def create_app(test_config=None):
    from . import status_page

    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'status_page_app.sqlite'),
    )
    CORS(app, resources={r"/.*": {"origins": "*"}})
    app.config['CORS_HEADERS'] = 'Content-Type'

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_prefixed_env()
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)
    init_errorhandler(app)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    InfluxDB.init_app(app)

    app.register_blueprint(status_page.bp)

    return app
