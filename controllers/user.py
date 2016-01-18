@auth.requires_login()
def index():
    return dict()


@auth.requires_login()
def request():
    return dict()


def login():
    return dict()

@auth.requires_login()
def my_vms():
    try:
        vms = conn.baadal_vms()
        response = list()
        for vm in vms:
            vm_properties = vm.properties()
            snapshots = vm.properties()['snapshots']
            for index in range(0, len(snapshots)):
                snapshots[index]['created'] = convert_timezone(snapshots[index]['created'])
            vm_properties['snapshots'] = snapshots
            response.append(vm_properties)
        return jsonify(data=response)
    except Exception as e:
        logger.error(e.message or str(e.__class__))
        return jsonify(status='fail')


@auth.requires_login()
def vm_status():
    vmid = request.vars.vmid
    vm = conn.find_baadal_vm(id=vmid)
    if vm:
        return jsonify(vm_status=vm.get_status())


@auth.requires_login()
def my_requests():
    rows = db(db.vm_requests.owner == session.username).select()
    l = rows.as_list()
    for i in l:
        i['flavor'] = flavor_info(i['flavor'])
        i['sec_domain'] = network_name_from_id(i['sec_domain'])
        i['request_time'] = seconds_to_localtime(i['request_time'])
        i['public_ip_required'] = 'Required' if i['public_ip_required'] == 1 else 'Not Required'
    return jsonify(data=l)


@auth.requires_login()
def my_requests_list():
    return dict()
