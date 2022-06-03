
from flask import (
    Blueprint, abort, render_template
)
from status_page_app.error_handler import Unauthorized, BadRequest, ServerError
from status_page_app import InfluxDB
import status_page_app.utils

bp = Blueprint('status', __name__, url_prefix='/')


@bp.route('/', methods=(['GET']))
def status():
    try:
        services = InfluxDB.connection.query(
            'show tag values from "metrics" with key = "service" WHERE ("host" = \'statuspage\' AND "performanceLabel" = \'nagiostatus\')')
        services_status = status_page_app.utils.get_services_list_from_resultset(
            services.raw['series'])

        results = InfluxDB.connection.query(
            'SELECT last("value") FROM "metrics" WHERE ("host" = \'statuspage\' AND "performanceLabel" = \'nagiostatus\') GROUP BY "service"')
        services_status, overall_status = status_page_app.utils.get_services_status_from_resultset(
            results.raw['series'], services_status)

        return render_template('body.html', services_status=services_status, overall_status=overall_status)
    except KeyError as e:
        abort(400, description=e)
    except BadRequest as e:
        abort(400, description=e.description)
    except Unauthorized as e:
        abort(401, description=e.description)
    except ServerError as e:
        abort(500, description=e.description)
