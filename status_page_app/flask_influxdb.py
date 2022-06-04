__all__ = ("FlaskInfluxDB")

from influxdb import InfluxDBClient
from flask import _app_ctx_stack


class FlaskInfluxDB(object):

    """Manages InfluxDB connections for your Flask app.
    FlaskInflux objects provide access to InfluxDB server via the :attr:`db`
    attribute. You must either pass the :class:`~flask.Flask`
    app to the constructor, or call :meth:`init_app`.
    """

    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        self.app = app
        app.teardown_appcontext(self.teardown)

    def connect(self):

        host = self.app.config.get("InfluxDB_HOST", None)
        db_name = self.app.config.get("InfluxDB_DB", None)
        db_port = self.app.config.get("InfluxDB_PORT", 8086)
        db_username = self.app.config.get("InfluxDB_USERNAME", None)
        db_password = self.app.config.get("InfluxDB_PSW", None)

        if host is None:
            raise ValueError(
                "You must set the Influx_HOST Flask config variable",
            )
        if db_name is None:
            raise ValueError(
                "You must set the InfluxDB_DB Flask config variable",
            )
        # Initialize the client for InfluxDB.
        client = InfluxDBClient(host=host, port=db_port,
                                username=db_username, password=db_password,
                                database=db_name)

        return client

    def teardown(self, exception):
        ctx = _app_ctx_stack.top
        if hasattr(ctx, 'Influx_db'):
            del ctx.Influx_db

    @property
    def connection(self):
        ctx = _app_ctx_stack.top
        if ctx is not None:
            if not hasattr(ctx, 'Influx_db'):
                ctx.Influx_db = self.connect()
            return ctx.Influx_db
