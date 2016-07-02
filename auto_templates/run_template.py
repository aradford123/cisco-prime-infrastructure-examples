#!/usr/bin/env python
from __future__ import print_function
import requests
import json
from argparse import ArgumentParser
from get_devices import device_by_ip, device_to_id
from get_template import get_template_by_name, build_template
from configure_interface import submit_template_job, wait_for_job, get_full_history

requests.packages.urllib3.disable_warnings()
from pi_config import PI, USER, PASSWORD
import logging
logger = logging.getLogger(__name__)

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

def process_template(template, options, device_ip):
    # find an augment the template
    template_schema = get_template(template)
    merge_template_vars(template_schema, options)

    # get the device
    device = device_by_ip(device_ip)
    device_id =  device_to_id(device)

    template_schema["cliTemplateCommand"]["targetDevices"]["targetDevice"]["targetDeviceID"] = device_id
    # modifies dict...
    print ("Applying template:'{template}' to device:{device}".format(template=template, device=device_ip))
    logger.debug("Device {device:} Applying template {template}".format(device=device_id, template=json.dumps(template_schema, indent=2)))

    job = submit_template_job(BASE, template_schema)

    logger.debug(json.dumps(job, indent=2))

    jobname = job['mgmtResponse']['cliTemplateCommandJobResult']['jobName']
    jobmessage = job['mgmtResponse']['cliTemplateCommandJobResult']['message']
    print("{jobmessage}\nWaiting for Job:{jobname}".format(jobmessage=jobmessage,jobname=jobname))
    print("\n")

    jobresponse = wait_for_job(BASE, jobname)
    job_status = jobresponse['queryResponse']['entity'][0]["jobSummaryDTO"]
    logger.debug(json.dumps(jobresponse, indent=2))

    print('user:{username} run:{runStatus} result:{resultStatus} Start:{lastStartTime} Stop:{completionTime}'.
          format(username=job_status['username'], resultStatus=job_status['resultStatus'],
                 runStatus=job_status['runStatus'],
                 lastStartTime=job_status['lastStartTime'],
                 completionTime=job_status['completionTime']))



    history = get_full_history(BASE, jobname)
    logger.debug(json.dumps(history, indent=2))

    if job_status['resultStatus'] == "SUCCESS":
        print('For full job history: op/jobService/runhistory.json?jobName={jobname}'.format(jobname=jobname))
    else:
        print ("job history:", json.dumps(history['mgmtResponse']['job']['runInstances']['runInstance']['results']['result'], indent=2))



if __name__ == "__main__":
    parser = ArgumentParser(description='Select options.')
    parser.add_argument('-t', type=str, required=True,
                        help="template name")
    parser.add_argument('-d', type=str,
                        help="device  ip address")
    parser.add_argument('-p', type=str, required=True,
                        help="parameters for template: as a python dict "
                             "e.g. '{\"arg1\" : \"val1\", \"arg2\" :\"val2\"}'  or '{}' for empty params")
    parser.add_argument('-v', action='store_true',
                        help="verbose")
    args = parser.parse_args()
    if args.v:
        logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

    process_template(args.t, json.loads(args.p), args.d)