# Openstack Limits Exporter
Prometheus exporter for openstack limits of specified projects

## Installation
```
pip install limits-exporter
```
In the examples folder exists a sample systemd unit file template.

## Usage
The exporter needs a `clouds.yaml` file, which is located at:
- `/etc/openstack/clouds.yaml`
- `~/.config/openstack/clouds.yaml`
- `./clouds.yaml`
- or at a custom location set with `export OS_CLIENT_CONFIG_FILE=/path/to/clouds.yaml`

Optional arguments are:
- `--clouds` only use clouds in comma-seperated list from `clouds.yaml` (default all)
- `--interval` the scrape interval in seconds (default 10s)
- `--port` the port on which the server runs (default 9500)

## More Information
- https://docs.openstack.org/python-openstackclient/latest/configuration/index.html


