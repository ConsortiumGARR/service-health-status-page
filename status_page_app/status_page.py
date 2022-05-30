
from flask import (
    Blueprint, flash, g, redirect, request, session, url_for, jsonify, abort, make_response
)
from status_page_app.error_handler import Unauthorized, BadRequest, ServerError, ResourceNotFound
import json
from flask_cors import CORS
from status_page_app import InfluxDB

bp = Blueprint('status', __name__, url_prefix='/')


@bp.route('/', methods=(['GET']))
def status():
    try:
        results = InfluxDB.connection.query('SELECT last("value") FROM "metrics" WHERE ("host" = \'statuspage\' AND "performanceLabel" = \'nagiostatus\') AND time >= now() - 1h GROUP BY time(30s), "service"')
        print(results)
        result = {}
        return jsonify(result)
    except KeyError as e:
        abort(400, description=e)
    except BadRequest as e:
        abort(400, description=e.description)
    except Unauthorized as e:
        abort(401, description=e.description)
    except ServerError as e:
        abort(500, description=e.description)