#!/usr/bin/env python

import requests
import json
from argparse import ArgumentParser

requests.packages.urllib3.disable_warnings()
from pi_config import PI, USER, PASSWORD

BASE="https://%s:%s@%s/webacs/api/v1/" %(USER,PASSWORD,PI)

def show_all_templates():
    result = requests.get(BASE + "data/CliTemplate.json?.full=true&.firstResult=0&.maxResults=1000", verify=False)
    result.raise_for_status()
    for template in result.json()['queryResponse']['entity']:
        print template['cliTemplateDTO']['@displayName'],template['cliTemplateDTO']['name']

def make_schema(template_name, variables):
    print """
{
  "cliTemplateCommand" : {
    "targetDevices" : {
      "targetDevice" : {
        "targetDeviceID" : "<DEVICEID>",
        "variableValues" : {
          "variableValue": [
    """
    for var in variables:
        if var['required']:
            print "                   #required"
        print '                { "name": "%s", "value" : None }' % var['name']
    print """
              ]
        }
      }
    },
    "templateName" : "%s"
  }
}
""" % template_name

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

    return result.json()

def get_template_by_id(template_id):
    '''
    :param nubmer id template: the template to show.
    :return:
    '''

    result = requests.get(BASE + "data/CliTemplate/%s.json?.full=true" % template_id, verify=False)
    result.raise_for_status()
    return json.dumps(result.json(), indent=2)

def show_template(template_id, template_name, schema):
    if template_id is not None:
        template = get_template_by_id(template_id)
    elif template_name is not None:
        template = get_template_by_name(template_name)

    if schema:
        print build_template(template)
    else:
        print json.dumps(template, indent=2)

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
