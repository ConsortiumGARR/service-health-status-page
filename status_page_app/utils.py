from datetime import datetime, timezone
import json, os

def init_services_list(base_list):
    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    json_url = os.path.join(SITE_ROOT, "data", "svc.json")
    base_list = json.load(open(json_url))
   
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
