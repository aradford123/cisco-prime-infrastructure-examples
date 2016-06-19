## Prime Infrastructure Configuration Templates examples

This directory contains some example python code for using configuration templates.

### configure_interface.py
is a script that applies the "Configure Interface" template to a device with the id of 610622.  It sets the interface "gig1/0/2" to access mode and assigns it to vlan 8.  It also updates the description.

You should change this for your example

### get_devices.py
gets a list of devices and their ID from the PI inventory.

``` bash
$ ./get_devices.py 
Getting all devices
ID     IP address
610619 10.10.10.115
610620 10.10.7.2
610621 100.1.1.5
610622 10.10.8.100
```

### pi_config.py
contains the credendials for the API user in PI

### get_template.py
by default will get a list of all templates and the ID.

use the "-t <id> -s" combination to see a schema (in JSON) for the template.  You can use this in a python script to simplify the code for deploying a template
It also tells you which template variables are essential

``` bash
$ python get_template.py -t 541541 -s
{
  "cliTemplateCommand": {
    "targetDevices": {
      "targetDevice": {
        "targetDeviceID": "<DEVICEID>", 
        "variableValues": {
          "variableValue": [
            {
              "name": "Description", 
              "value": ""
            }, 
            {
              "name": "InterfaceName", 
              "value": "required"
            }, 
            {
              "name": "NativeVLan", 
              "value": ""
            }, 
            {
              "name": "StaticAccessVLan", 
              "value": ""
            }, 
            {
              "name": "TrunkAllowedVLan", 
              "value": ""
            }, 
            {
              "name": "VoiceVlan", 
              "value": ""
            }, 
            {
              "name": "spd", 
              "value": ""
            }, 
            {
              "name": "A1", 
              "value": ""
            }, 
            {
              "name": "duplexField", 
              "value": ""
            }, 
            {
              "name": "PortFast", 
              "value": ""
            }
          ]
        }
      }
    }, 
    "templateName": "Configure Interface"
  }
}


```

