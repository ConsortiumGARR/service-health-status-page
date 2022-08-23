from datetime import datetime, timezone
import json
import os
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from status_page_app.error_handler import *


def request_data():
    try:
        session = requests.Session()
        retry = Retry(connect=6, backoff_factor=0.5)
        adapter = HTTPAdapter(max_retries=retry)
        session.mount('http://', adapter)
        session.mount('https://', adapter)
        url = 'https://swift.cloud.garr.it/swift/v1/neanias-status-page/status-page-data.json'
        resp = session.get(url)
    except (requests.ConnectionError, requests.Timeout, requests.TooManyRedirects, requests.URLRequired) as e:
        raise ServerError('Object Storage connection error: ' + str(e))
    try:
        resp.raise_for_status()
    except requests.HTTPError as e:
        if e.response.status_code == 400:
            raise BadRequest(description=e.response.text)
        elif e.response.status_code == 401:
            raise Unauthorized(description=e.response.text)
        elif e.response.status_code == 404:
            raise ResourceNotFound(description=e.response.text)
        else:
            raise ServerError(description=e.response.text)
    try:
        ctype = resp.headers['content-type']
    except KeyError:
        # success but no content
        return None, resp.headers
    if 'application/json' in ctype:

        return resp.json(), resp.headers
    else:
        return resp.text, resp.headers


def init_services_list(base_list):
    base_list, resp_code = request_data()
    for s in base_list:
        base_list[s]['status'] = None
    return base_list


def services_status_from_resultset(resultset, service_map):

    overall_status = True
    for r in resultset:
        service_name = r['tags']['service']
        status = int(r['values'][0][1])
        if service_name in service_map:
            service_map[service_name]['status'] = status
            service_map[service_name]['date'] = r['values'][0][0]
            try:
                dt_obj = datetime.strptime(
                    service_map[service_name]['date'], "%Y-%m-%dT%H:%M:%S%z")
                delta_update = datetime.now(timezone.utc) - dt_obj
                if delta_update.days >= 1:  # if more than 24h
                    service_map[service_name]['status'] = 3
            except Exception as e:
                print(e)
            if service_map[service_name]['status'] != 0:
                overall_status = False

    return service_map, overall_status
