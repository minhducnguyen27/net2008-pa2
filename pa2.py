#Name: Minh Duc Nguyen 
#Student ID: 040844107

#!/usr/bin/env python3



import sys
import json
import xml.etree.ElementTree as ET
from pathlib import Path
import yaml



class AuditError(Exception): #Custom exception class for policy or parsing errors during the audit.
    def __init__(self, message,filename=None):
        super().__init__(message)
        self.filename = filename

class FleetAuditor: #Class representing the network fleet compliance auditor
    def __init__(self,xml_path: str, yaml_path: str):
        self.xml_path = Path(xml_path)
        self.yaml_path = Path(yaml_path)
        self.policy={}
        self.site=None
        self.total_devices = 0
        self.skipped_devices = 0
        self.roles = {}
        self.interface_count={"up":0,"down":0,"other":0}
        self.devics = []

def load_files(self)->None: # Safely load and validate both the XML inventory and YAML policy files
    if not self.xml_path.exists() or not self.yaml_path.exists():
        raise AuditError("Input files do not exist")
    
    # Load YAML policy
    try:
        with open(self.yaml_path,"r",encoding="utf-8") as f:
            self.policy = yaml.safe_load(f)
            if not isinstance(self.policy, dict):
                raise AuditError("Policy is not valid")
    except yaml.YAMLError as e:
        raise AuditError((f"Invalid YAML format: {e}",self.yaml_path.name))
    except Exception as e:
        raise AuditError(f"Error reading policy file: {e}",self.yaml_path.name)
        
    
    # Parse XML inventory
    try: 
        tree = ET.parse(self.xml_path)
        root = tree.getroot()
    except ET.ParseError as e:
        raise AuditError((f"Invalid XML format: {e}",self.xml_path.name))
    except Exception as e:
        raise AuditError(f"Error Parsing XML inventory: {e}",self.xml_path.name)
    
    self.site = root.get("site",None)
    
    for device in root.findall("device"):
        device_id = device.get("id")
    
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
    
    