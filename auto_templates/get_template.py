#!/usr/bin/env python

from __future__ import print_function
import requests
import json

from argparse import ArgumentParser

requests.packages.urllib3.disable_warnings()
from pi_config import PI, USER, PASSWORD

BASE="https://%s:%s@%s/webacs/api/v1/" %(USER,PASSWORD,PI)

class NoTemplateFound(Exception):
    pass

def show_all_templates():
    result = requests.get(BASE + "data/CliTemplate.json?.full=true&.firstResult=0&.maxResults=1000", verify=False)
    result.raise_for_status()
    for template in result.json()['queryResponse']['entity']:
        print (template['cliTemplateDTO']['@displayName'],template['cliTemplateDTO']['name'])



def make_schema(template_name, variables):

    template = {
     "cliTemplateCommand" : {
       "targetDevices" : {
         "targetDevice" : {
           "targetDeviceID" : "<DEVICEID>",
           "variableValues" : {
             "variableValue": [ ]
           }
         }
       },
     "templateName" : ""
     }
    }

    # single variable need to be turned into a list
    if isinstance(variables, dict):
        variables = [variables]
    vars = [ {"name" : var['name'], "value" : "required" if var['required'] else  ""} for var in variables]
    template['cliTemplateCommand']['templateName'] = template_name
    template['cliTemplateCommand']['targetDevices']["targetDevice"]["variableValues"]["variableValue"] = vars

    return template

def build_template(cli_template):
    return make_schema(cli_template['queryResponse']['entity'][0]['cliTemplateDTO']['name'],
                    cli_template['queryResponse']['entity'][0]['cliTemplateDTO']['variables']['variable'])

def get_template_by_name(template_name):
    '''
    :param  name of template: the template to show.
    :return:
    '''

    result = requests.get(BASE + 'data/CliTemplate.json?.full=true&name="%s"' % template_name, verify=False)
    result.raise_for_status()
    if result.json()["queryResponse"]["@count"] == "1":
        return result.json()
    else:
        raise NoTemplateFound("Cannot find template called: %s" % template_name)

def get_template_by_id(template_id):
    '''
    :param nubmer id template: the template to show.
    :return:
    '''

    result = requests.get(BASE + "data/CliTemplate/%s.json?.full=true" % template_id, verify=False)

    try:
        result.raise_for_status()
        return result.json()
    except requests.exceptions.HTTPError:
        raise NoTemplateFound("Cannot find template number: %s" % template_id)

def show_template(template_id, template_name, schema):
    if template_id is not None:
        template = get_template_by_id(template_id)
    elif template_name is not None:
        template = get_template_by_name(template_name)

    if schema:
        print (json.dumps(build_template(template), indent=2))
    else:
        print (json.dumps(template,indent=2))

if __name__ == "__main__":
    parser = ArgumentParser(description='Select options.')
    parser.add_argument('-t', type=str,
                        help="template id")
    parser.add_argument('-n', type=str, help="template by name")
    parser.add_argument('-s', action="store_true",
                        help="template schema")

    args = parser.parse_args()

    if args.t is not None or args.n is not None:
        show_template(args.t, args.n, args.s)
    else:
        show_all_templates()
