#!/usr/bin/env python

import requests
import json
requests.packages.urllib3.disable_warnings()
from pi_config import PI, USER, PASSWORD

BASE="https://%s:%s@%s/webacs/api/v1/" %(USER,PASSWORD,PI)


result = requests.get(BASE + "data/Devices.json", verify=False)
result.raise_for_status()
print json.dumps(result.json(), indent=2)

print "Getting a specific device"
result = requests.get(BASE + "data/Devices/610622.json?.full=true", verify=False)
result.raise_for_status()
print json.dumps(result.json(), indent=2)

print "Getting a specific device by IP address"
result = requests.get(BASE + "data/Devices.json?ipAddress=%s" % '10.10.8.100', verify=False)
result.raise_for_status()
print json.dumps(result.json(), indent=2)