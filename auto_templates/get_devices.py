#!/usr/bin/env python

import requests
import json
from argparse import ArgumentParser

requests.packages.urllib3.disable_warnings()
from pi_config import PI, USER, PASSWORD

BASE="https://%s:%s@%s/webacs/api/v1/" %(USER,PASSWORD,PI)

def all_devices():
    print "Getting all devices"
    print "{0:6s} {1:10s}".format("ID", "IP address")
    result = requests.get(BASE + "data/Devices.json?.full=true", verify=False)
    result.raise_for_status()
    for device in result.json()['queryResponse']['entity']:
        print device['devicesDTO']['@id'], device['devicesDTO']['ipAddress']

def device_by_id(id):
    print "Getting a specific device"
    result = requests.get(BASE + "data/Devices/%s.json?.full=true" % id, verify=False)
    result.raise_for_status()
    print json.dumps(result.json(), indent=2)

def device_by_ip(ip):
    print "Getting a specific device by IP address"
    result = requests.get(BASE + "data/Devices.json?.full=true&ipAddress=%s" % ip, verify=False)
    result.raise_for_status()
    print json.dumps(result.json(), indent=2)



if __name__ == "__main__":
    parser = ArgumentParser(description='Select options.')
    parser.add_argument('--id', type=str,
                        help="device details by id")
    parser.add_argument('--ip', type=str,
                        help="device details by ip address")
    args = parser.parse_args()

    if args.id:
        device_by_id(args.id)
    elif args.ip:
        device_by_ip(args.ip)
    else:
        all_devices()
