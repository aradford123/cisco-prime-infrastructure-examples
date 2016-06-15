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
        print '                { "name": "%s", "value" : NONE }' % var['name']
    print """
              ]
        }
      }
    },
    "templateName" : "%s"
  }
}
""" % template_name

def show_a_template(template, schema):
    '''
    :param number: the template to show.  541541 was the configure_interface template
    :return:
    '''
    result = requests.get(BASE + "data/CliTemplate/%s.json?.full=true" % template, verify=False)
    result.raise_for_status()
    if not schema:
        print json.dumps(result.json(), indent=2)
    else:
        make_schema(result.json()['queryResponse']['entity'][0]['cliTemplateDTO']['name'],
                    result.json()['queryResponse']['entity'][0]['cliTemplateDTO']['variables']['variable'])

def show_template(template, schema):
    if template == None:
        show_all_templates()
    else:
        show_a_template(template, schema)

if __name__ == "__main__":
    parser = ArgumentParser(description='Select options.')
    parser.add_argument('-t', type=str,
                        help="template details")
    parser.add_argument('-s', action="store_true",
                        help="template schema")

    args = parser.parse_args()
    show_template(args.t, args.s)