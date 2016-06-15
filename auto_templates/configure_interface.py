#!/usr/bin/env python

import requests
import json
import time
requests.packages.urllib3.disable_warnings()

from pi_config import PI, USER, PASSWORD
BASE="https://%s:%s@%s/webacs/api/v1/" %(USER,PASSWORD,PI)


CLI_TEMPLATE = {
  "cliTemplateCommand" : {
    "targetDevices" : {
      "targetDevice" : {
        "targetDeviceID" : "610622",
        "variableValues" : {
          "variableValue": [
            {
              "name": "InterfaceName",
              "value": "gigabitethernet1/0/2"
            },
            {
              "name": "Description",
              "value": "Fred1"
            },
            {
              "name": "StaticAccessVLan",
              "value": "8"
            },
            {
              "name": "A1",
              "value": "Access"
            },
            { "name": "NativeVLan", "value": None},
            { "name": "duplexField","value": None},
            { "name": "TrunkAllowedVLan","value": None },
            { "name": "spd","value": None },
            { "name": "VoiceVlan" ,"value": None},
            { "name": "PortFast","value": None }
          ]

        }
      }
    },
    "templateName" : "Configure Interface"
  }
}


def get_job_status(jobname):
    url = BASE + 'data/JobSummary.json?jobName=%s' %jobname
    jobresult = requests.get(url, verify=False)
    jobresult.raise_for_status()
    return jobresult.json()

def get_job_detail(jobnumber):
    url = BASE + 'data/JobSummary/%s.json' %jobnumber
    jobresult = requests.get(url, verify=False)
    jobresult.raise_for_status()
    return jobresult.json()

def get_full_history(jobname):
    url = BASE + 'op/jobService/runhistory.json?jobName=%s' %jobname
    jobresult = requests.get(url, verify=False)
    jobresult.raise_for_status()
    return jobresult.json()

def wait_for_job(jobname):
    while True:

        result = get_job_status(jobname)

        status = result['queryResponse']['entityId'][0]['@displayName'].split(",")[-1]

        if status == "SCHEDULED":
            print status
            time.sleep(5)
        else:
            json.dumps(result)
            jobnumber = result['queryResponse']['entityId'][0]['$']
            jobdetail = get_job_detail(jobnumber)
            print json.dumps(jobdetail, indent=2)
            return jobdetail


def main():

    headers={"Content-Type" : "application/json"}
    result = requests.put(BASE + "op/cliTemplateConfiguration/deployTemplateThroughJob.json", headers=headers,
                        data=json.dumps(CLI_TEMPLATE), verify=False)
    result.raise_for_status()
    print json.dumps(result.json(), indent=2)

    jobname = result.json()['mgmtResponse']['cliTemplateCommandJobResult']['jobName']
    wait_for_job(jobname)

    history = get_full_history(jobname)
    print json.dumps(history, indent=2)

if __name__ == "__main__":
    main()