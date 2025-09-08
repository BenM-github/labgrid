import requests

# Driver has been tested with:
# * Gude Expert Power Control 8031-1
# This device needs to be used in 'Basic Compatible' mode for HTTP GET
# to be usable. Do not turn on session authentication.
#
# HTTP-GET API is defined in the Gude EPC-HTTP-Interface specification:
# http://wiki.gude.info/EPC_HTTP_Interface
#
# The `components=<N>` parameter defines which status information are
# included into the returned JSON.
# * `components=0` happily returns an empty response but still switches the
#   outputs as requested.
# * `components=1` only includes the output's state into the JSON.

PORT = 80


def power_set(host, port, index, value):
    index = int(index)
    range = count_ports(host, port)
    assert 1 <= index <= range, f'index ({index}) out of range (1-{range})'
    # access the web interface...
    value = 1 if value else 0
    r = requests.get(f"http://{host}:{port}/status.json?components=0&cmd=1&p={index}&s={value}")
    r.raise_for_status()


def power_get(host, port, index):
    index = int(index)

    # get the component status
    r = requests.get(f"http://{host}:{port}/status.json?components=1")
    r.raise_for_status()

    range = count_ports(host, port)
    assert 1 <= index <= range, f'index ({index}) out of port range (1-{range})'
    state = r.json()["outputs"][index - 1]["state"]

    return state


# unsicher ob nötig oder nicht zu viel overhead
def count_ports(host, port):
    r = requests.get(f"http://{host}:{port}/status.json?components=1")
    r.raise_for_status()
    return len(r.json()["outputs"])