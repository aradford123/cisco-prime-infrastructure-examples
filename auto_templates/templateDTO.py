template ={
  "queryResponse": {
    "@responseType": "getEntity",
    "entity": [
      {
        "cliTemplateDTO": {
          "lastDeployTime": "2016-05-22T12:09:07.096+10:00",
          "@displayName": "541541",
          "description": "Configure Interface",
          "author": "Cisco Systems",
          "createdOn": "2016-05-15T16:00:10.680+10:00",
          "deployCount": 2,
          "content": "#if (${InterfaceName})\n        interface ${InterfaceName}\n       #if (${Description} != \"\")\n            description ${Description}\n        #end\n        #if(${A1}  == \"Access\")\n            switchport mode access\n            #if(${StaticAccessVLan} != \"\")\n                switchport ACCess vlan ${StaticAccessVLan}   \n            #end\n        #end\n        \n       #if(${A1}  == \"Trunk\")\n            switchport mode trunk\n            #if(${TrunkAllowedVLan} != \"\")\n                switchport trunk allowed vlan ${TrunkAllowedVLan}   \n            #end\n            #if(${NativeVLan} != \"\")\n                switchport trunk native vlan ${NativeVLan}   \n            #end\n        #end\n        \n        #if(${A1}  == \"Dynamic Auto\")\n            switchport mode dynamic auto\n        #end\n\n        #if(${A1}  == \"Dynamic Desirable\")\n            switchport mode dynamic desirable\n        #end\n\n        #if(${VoiceVlan} != \"\")\n             switchport voice vlan ${VoiceVlan}\n        #end\n\n        #if(${PortFast} != \"\")\n               #if(${PortFast}  == \"Disable\")\n                   no spanning-tree portfast   \n               #elseif(${PortFast}  == \"Enable\")\n                   spanning-tree portfast              \n               #end\n        #end\n\n         #if(${spd}!= \"\")\n               #if(${spd}  == \"Auto\")\n                   speed auto   \n               #elseif(${spd}  == \"10 Mbps\")\n                   speed 10\n               #elseif(${spd}  == \"100 Mbps\")\n                    speed 100\n                #elseif(${spd}  == \"1000 Mbps\")\n                    speed 1000\n               #end\n        #end\n\n        #if(${duplexField}!= \"\")\n               #if(${duplexField}  == \"Auto\")\n                   duplex auto   \n               #elseif(${duplexField}  == \"Half\")\n                   duplex half\n               #elseif(${duplexField}  == \"Full\")\n                   duplex full\n               #end\n        #end\nexit\n#end\n\n\n\n\n\n\n\n\n",
          "deviceType": "Switches and Hubs,Wireless Controller/Cisco 5760 Series Wireless LAN Controller",
          "templateId": 541541,
          "path": "CLI Templates/System Templates - CLI",
          "@id": "541541",
          "variables": {
            "variable": [
              {
                "displayLabel": "Description",
                "required": False,
                "type": "String",
                "description": "Description",
                "name": "Description"
              },
              {
                "displayLabel": "Interface Name",
                "required": True,
                "type": "String",
                "description": "Interface Name",
                "name": "InterfaceName"
              },
              {
                "displayLabel": "Native VLan",
                "required": False,
                "type": "Integer",
                "description": "Native VLan",
                "name": "NativeVLan"
              },
              {
                "displayLabel": "Static Access VLan",
                "required": False,
                "type": "Integer",
                "description": "Static Access VLan",
                "name": "StaticAccessVLan"
              },
              {
                "displayLabel": "Trunk Allowed VLan",
                "required": False,
                "type": "Integer",
                "description": "Trunk Allowed VLan",
                "name": "TrunkAllowedVLan"
              },
              {
                "displayLabel": "VLan for Voice Traffic",
                "required": False,
                "type": "Integer",
                "description": "VLan for Voice Traffic",
                "name": "VoiceVlan"
              },
              {
                "displayLabel": "Interface Speed",
                "description": "10 Mbps,100 Mbps,1000 Mbps,Auto,No Change",
                "defaultValue": "10 Mbps,100 Mbps,1000 Mbps,Auto,NoChange",
                "required": False,
                "type": "Dropdown",
                "name": "spd"
              },
              {
                "displayLabel": "Administrative Mode",
                "description": "Access,Dynamic Auto,Dynamic Desirable,No Change,Trunk",
                "defaultValue": "Access,Dynamic Auto,Dynamic Desirable,No Change,Trunk",
                "required": False,
                "type": "Dropdown",
                "name": "A1"
              },
              {
                "displayLabel": "Duplex",
                "description": "Auto,Full,Half,No Change",
                "defaultValue": "Auto,Full,Half,NoChange",
                "required": False,
                "type": "Dropdown",
                "name": "duplexField"
              },
              {
                "displayLabel": "Port Fast",
                "description": "Disable,Enable,No Change",
                "defaultValue": "Disable,Enable,NoChange",
                "required": False,
                "type": "Dropdown",
                "name": "PortFast"
              }
            ]
          },
          "name": "Configure Interface"
        },
        "@url": "https://adam-pi/webacs/api/v1/data/CliTemplate/541541",
        "@type": "CliTemplate",
        "@dtoType": "cliTemplateDTO"
      }
    ],
    "@rootUrl": "https://adam-pi/webacs/api/v1/data",
    "@type": "CliTemplate",
    "@requestUrl": "https://adam-pi/webacs/api/v1/data/CliTemplate/541541?.full=true"
  }
}