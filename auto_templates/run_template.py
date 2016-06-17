import requests
import json
from argparse import ArgumentParser
from get_devices import device_by_ip, device_to_id
from get_template import get_template_by_name, build_template

requests.packages.urllib3.disable_warnings()
from pi_config import PI, USER, PASSWORD

BASE="https://%s:%s@%s/webacs/api/v1/" %(USER,PASSWORD,PI)

def process_template(device_ip, template, options):
    device = device_by_ip(device_ip)
    device_id =  device_to_id(device)

    template = get_template_by_name(template)
    template_schema = build_template(template)

   # print template_schema['cliTemplateCommand']
    #template_schema["cliTemplateCommand"]["targetDevices"]["targetDevice"]["targetDeviceID"] = device_id
    print device_id, template_schema

if __name__ == "__main__":
    parser = ArgumentParser(description='Select options.')
    parser.add_argument('-t', type=str,
                        help="template name")
    parser.add_argument('-d', type=str,
                        help="device  ip address")
    args = parser.parse_args()
    options= ""
    process_template(args.d, args.t, options)