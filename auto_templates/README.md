## Prime Infrastructure Configuration Templates examples

This directory contains some example python code for using configuration templates.

### configure_interface.py
is a script that applies the "Configure Interface" template to a device with the id of 610622.  You should change this for your example

### get_devices.py
gets a list of devices and their ID from the PI inventory.

### pi_config.py
contiains the credendials for the API user in PI

### get_template.py
by default will get a list of all templates and the ID.

use the "-t <id> -s" combination to see a schema (in JSON) for the template.  You can use this in a python script to simplify the code for deploying a template
It also tells you which template variables are essential

``` bash
$ python get_template.py -t 541541 -s

{
  "cliTemplateCommand" : {
    "targetDevices" : {
      "targetDevice" : {
        "targetDeviceID" : "<DEVICEID>",
        "variableValues" : {
          "variableValue": [
    
                { "name": "Description", "value" : NONE }
                   #required
                { "name": "InterfaceName", "value" : NONE }
                { "name": "NativeVLan", "value" : NONE }
                { "name": "StaticAccessVLan", "value" : NONE }
                { "name": "TrunkAllowedVLan", "value" : NONE }
                { "name": "VoiceVlan", "value" : NONE }
                { "name": "spd", "value" : NONE }
                { "name": "A1", "value" : NONE }
                { "name": "duplexField", "value" : NONE }
                { "name": "PortFast", "value" : NONE }

              ]
        }
      }
    },
    "templateName" : "Configure Interface"
  }
}

```

