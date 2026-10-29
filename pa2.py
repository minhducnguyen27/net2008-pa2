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

def load_files(self)->None: 
    
