
def services_list_from_resultset(resultset):
    res = {}
    for v in resultset[0]['values']:
        service_name = v[1]
        res[service_name] = {'status': None}
    return res


def services_status_from_resultset(resultset, service_map):
    overall_status = True
    for r in resultset:
        service_name = r['tags']['service']
        # TODO add multiple checks
        status = int(r['values'][0][1])
        service_map[service_name]['status'] = status
        service_map[service_name]['date'] = r['values'][0][0]
        if status != 0:
            overall_status = False
    return service_map, overall_status
