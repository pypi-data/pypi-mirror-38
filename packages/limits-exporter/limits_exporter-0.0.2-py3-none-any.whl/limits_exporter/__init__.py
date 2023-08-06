from functools import reduce
from time import sleep

from openstack import connect
from openstack.config import OpenStackConfig
from prometheus_client import start_http_server
from prometheus_client.core import GaugeMetricFamily, REGISTRY


# metrics
# openstack_limit_cores[project_id='', view='max']
# openstack_limit_cores[project_id='', view='used']
# openstack_limit_floating_ips[project_id='', view='max']
# openstack_limit_floating_ips[project_id='', view='used']
# openstack_limit_instances[project_id='', view='max']
# openstack_limit_instances[project_id='', view='used']
# openstack_limit_ram[project_id='', view='max']
# openstack_limit_ram[project_id='', view='used']
# openstack_limit_security_groups[project_id='', view='max']
# openstack_limit_security_groups[project_id='', view='used']
# openstack_limit_server_groups[project_id='', view='max']
# openstack_limit_server_groups[project_id='', view='used']

LIMITS = {
    'cores': [
        {'view': 'max', 'attribute': 'max_total_cores'},
        {'view': 'used', 'attribute': 'total_cores_used'}
    ],
    'floating_ips': [
        {'view': 'max', 'attribute': 'properties.maxTotalFloatingIps'},
        {'view': 'used', 'attribute': 'properties.totalFloatingIpsUsed'}
    ],
    'instances': [
        {'view': 'max', 'attribute': 'max_total_instances'},
        {'view': 'used', 'attribute': 'total_instances_used'}
    ],
    'ram': [
        {'view': 'max', 'attribute': 'max_total_ram_size'},
        {'view': 'used', 'attribute': 'total_ram_used'}
    ],
    'security_groups': [
        {'view': 'max', 'attribute': 'properties.maxSecurityGroups'},
        {'view': 'used', 'attribute': 'properties.totalSecurityGroupsUsed'}
    ],
    'server_groups': [
        {'view': 'max', 'attribute': 'max_server_groups'},
        {'view': 'used', 'attribute': 'total_server_groups_used'}
    ]
}

def rget(obj, key, *args):
    def _get(obj, key):
        return obj.get(key, *args)
    return reduce(_get, [obj] + key.split('.'))

class Connection():
    conn = None
    limits = None

    def __init__(self, name):
        self.conn = connect(cloud=name)
        self.new_compute_limits()

    def get_compute_limits(self):
        return self.limits

    def new_compute_limits(self):
        self.limits = self.conn.get_compute_limits().toDict()


class LimitCollector():
    conns = {}
    name = ""

    def __init__(self, conns, name):
        self.conns = conns
        self.name = name

    def collect(self):
        metric = GaugeMetricFamily(
            "openstack_limit_%s" % self.name,
            "openstack limit for %s in project" % self.name,
            labels=["project_id", "view"]
        )

        for conn in self.conns:
            limits = conn.get_compute_limits()

            for val in LIMITS[self.name]:
                metric.add_metric(
                    [rget(limits, 'location.project.id'), val['view']],
                    rget(limits, val['attribute'])
                )

        yield metric


def start_server(port, interval, cloud_names):
    clouds = []
    if cloud_names is None:
        for cloud in OpenStackConfig().get_all():
            clouds.append(cloud.name)
    else:
        clouds = cloud_names.split(",")

    conns = []
    for cloud in clouds:
        conns.append(Connection(cloud))

    for name in LIMITS:
        collector = LimitCollector(conns, name)
        REGISTRY.register(collector)

    start_http_server(port)

    while True:
        for conn in conns:
            conn.new_compute_limits()
        sleep(interval)
