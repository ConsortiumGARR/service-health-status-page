
import imp
from flask import (
    Blueprint, abort, render_template
)
from status_page_app.error_handler import Unauthorized, BadRequest, ServerError
from status_page_app import InfluxDB
import status_page_app.utils
from influxdb.exceptions import InfluxDBClientError, InfluxDBServerError

bp = Blueprint('status', __name__, url_prefix='/')


@bp.route('/', methods=(['GET']))
def status():
    try:
        tags_query = 'SHOW tag values \
            FROM "metrics" with key = "service" \
            WHERE ("host" = \'statuspage\' AND \
                "performanceLabel" = \'nagiostatus\' AND "service" != \'hostcheck\')'
        svc_query = 'SELECT last("value") \
            FROM "metrics" \
            WHERE ("host" = \'statuspage\' \
                AND "performanceLabel" = \'nagiostatus\' ) \
            GROUP BY "service"'

        services = InfluxDB.connection.query(tags_query)
        svc_status = status_page_app.utils.\
            services_list_from_resultset(services.raw['series'])

        results = InfluxDB.connection.query(svc_query)
        svc_status, oa_status = status_page_app.utils.\
            services_status_from_resultset(results.raw['series'], svc_status)

        return render_template('body.html',
                               services_status=svc_status,
                               overall_status=oa_status)
    except KeyError as e:
        abort(400, description=e)
    except BadRequest as e:
        abort(400, description=e.description)
    except Unauthorized as e:
        abort(401, description=e.description)
    except ServerError as e:
        abort(500, description=e.description)
    except InfluxDBClientError as e:
        abort(500, description=e.content)
    except InfluxDBServerError as e:
        abort(500, description=e.content)
    except Exception as e:
        abort(500)
