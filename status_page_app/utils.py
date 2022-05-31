
def get_services_list_from_resultset(resultset):
    res = {}
    print(resultset)
    for v in resultset[0]['values']:
        service_name = v[1]
        res[service_name] = {'status': None}
    return res

def get_services_status_from_resultset(resultset, service_map):

    for r in resultset:
        service_name = r['tags']['service']
        #TODO add multiple checks
        service_map[service_name]['status'] = int(r['values'][0][1])
    return service_map