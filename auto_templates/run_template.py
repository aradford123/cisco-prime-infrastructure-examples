from __future__ import print_function
import requests
import json
from argparse import ArgumentParser
from get_devices import device_by_ip, device_to_id
from get_template import get_template_by_name, build_template
from configure_interface import submit_template_job, wait_for_job, get_full_history

requests.packages.urllib3.disable_warnings()
from pi_config import PI, USER, PASSWORD

BASE="https://%s:%s@%s/webacs/api/v1/" %(USER,PASSWORD,PI)

class RequiredVarsMissing(Exception):
   pass

# returns a copy of the merged list of dictionary.
def merge_vars(template_vars, provided_vars):

    merged = [var_dict.copy() for var_dict in template_vars]
    for var_dict in merged:
        if var_dict['name'] in provided_vars:
            var_dict['value'] = provided_vars[var_dict['name']]

    return merged

# should return a list of required vars not filled in
def required_vars_not_defined(var_dict_list):
    # look for any vars with a value of "required" as those need to be filled in
    return [ var_dict['name'] for var_dict in var_dict_list if var_dict['value'] is "required" ]

def merge_template_vars(template_schema, provided_vars):
    merged = merge_vars(
            template_schema['cliTemplateCommand']['targetDevices']["targetDevice"]["variableValues"]["variableValue"],
            provided_vars)
    required_vars_missing = required_vars_not_defined(merged)

    if len(required_vars_missing) == 0 :
        template_schema['cliTemplateCommand']['targetDevices']["targetDevice"]["variableValues"]["variableValue"] = merged
    else:
        raise RequiredVarsMissing("Missing vars: ", required_vars_missing)

def get_template(template):
    template = get_template_by_name(template)
    template_schema = build_template(template)
    return template_schema

def process_template(device_ip, template, options):
    # find an augment the template
    template_schema = get_template(template)
    merge_template_vars(template_schema, options)

    # get the device
    device = device_by_ip(device_ip)
    device_id =  device_to_id(device)

    template_schema["cliTemplateCommand"]["targetDevices"]["targetDevice"]["targetDeviceID"] = device_id
    # modifies dict...
    print ("Device {device:} Applying template {template}".format(device=device, template=json.dumps(template_schema, indent=2)))

    job = submit_template_job(BASE, template_schema)

    print(json.dumps(job, indent=2))

    jobname = job   ['mgmtResponse']['cliTemplateCommandJobResult']['jobName']
    jobresponse = wait_for_job(BASE, jobname)
    print(json.dumps(jobresponse, indent=2))

    history = get_full_history(BASE, jobname)
    print(json.dumps(history, indent=2))


if __name__ == "__main__":
    parser = ArgumentParser(description='Select options.')
    parser.add_argument('-t', type=str,
                        help="template name")
    parser.add_argument('-d', type=str,
                        help="device  ip address")
    parser.add_argument('-p', type=str,
                        help="parameters")
    args = parser.parse_args()

    process_template(args.d, args.t, json.loads(args.p))