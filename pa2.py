#!/usr/bin/env python3
#Name: Minh Duc Nguyen 
#Student ID: 040844107





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
        self.devices = []
        self.violations=[]
        self.compliant_ids=[]
        
    def load_files(self): # Safely load and validate both the XML inventory and YAML policy files
        if not self.xml_path.exists() or not self.yaml_path.exists():
            raise AuditError("Input files do not exist")
        
        # Load YAML policy
        try:
            with open(self.yaml_path,"r",encoding="utf-8") as f:
                self.policy = yaml.safe_load(f)
                if not isinstance(self.policy, dict):
                    raise AuditError("Policy is not valid")
        except yaml.YAMLError as e:
            raise AuditError(f"Invalid YAML format: {e}",self.yaml_path.name)
        except Exception as e:
            raise AuditError(f"Error reading policy file: {e}",self.yaml_path.name)
            
        
        # Parse XML inventory
        try: 
            tree = ET.parse(self.xml_path)
            root = tree.getroot()
        except ET.ParseError as e:
            raise AuditError(f"Invalid XML format: {e}",self.xml_path.name)
        except Exception as e:
            raise AuditError(f"Error Parsing XML inventory: {e}",self.xml_path.name)
        
        self.site = root.get("site",None)
        
        for device in root.findall("device"):
            device_id = device.get("id")
            
            if not device_id or not device_id.strip(): # A device with no id attribute is skipped and couted
                self.skipped_devices += 1 
                continue
            
            self.total_devices += 1 
            role = device.get("role")
            os_version = device.get("os")
            
            
            if role:
                self.roles[role] = self.roles.get(role,0) + 1 
            
            dev_interfaces = []
            for iface in device.findall("interface"):
                name = iface.get("name")
                status = iface.get("status","other")
                
                if status in self.interface_count:
                    self.interface_count[status] += 1 
                else:
                    self.interface_count["other"] += 1
                    
                dev_interfaces.append({"name":name,"status":status})
            
            owner_elem = device.find("owner")
            owner = owner_elem.text.strip() if (owner_elem is not None and owner_elem.text) else ""
            
            self.devices.append({
                "id": device_id,
                "role": role,
                "os":os_version,
                "owner": owner,
                "interface":dev_interfaces
                })
    
        
    def evaluate_policies(self): #Set up policies to evaluate devices
        min_os_policy = self.policy.get("min_os",{}) # check if the device have mininum OS
        require_owner_policy = self.policy.get("require_owner",False) # check if the device have owner
        max_down_policy = self.policy.get("max_down_interfaces",None) # check if the device have max down policy
        
        for dev in self.devices:
            dev_id = dev["id"]
            role = dev["role"]
            owner = dev["owner"]
            interfaces = dev["interface"]
            
            dev_violation = False
            
            if min_os_policy is not None: #Check for unknown role
                if role not in min_os_policy:
                    self.violations.append({
                        "device": dev_id,
                        "type":"unknown_role",
                        "role":role})
                    dev_violation = True
                        
            if require_owner_policy is True and not owner: # Check for missing onwer
                self.violations.append({
                    "device":dev_id,
                    "type":"missing_owner",
                    "none":None})
                dev_violation = True
                
            if max_down_policy is not None: # Check for max down
                down_count = sum (1 for link in interfaces if link["status"] == "down")
                if down_count > max_down_policy:
                    self.violations.append({
                        "device": dev_id,
                        "type":"too_many_down",
                        "down":down_count})
                    dev_violation = True
           
            if not dev_violation: # If no violations for device, add to compliant list
                self.compliant_ids.append(dev_id)
    
        self.compliant_ids.sort()
        
    def generate_report(self): #Process Tier 1 and Tier 2 and write the audit.json output file
        self.load_files()
        self.evaluate_policies()
        
        
        report = {
            "site": self.site,
            "total_devices": self.total_devices,
            "skipped_devices": self.skipped_devices,
            "roles":self.roles,
            "interfaces": self.interface_count,
            "violations":self.violations,
            "compliant":self.compliant_ids
            }
    
        output_path = Path("audit.json")
        try:
            with open(output_path,"w",encoding="utf-8") as f:
                json.dump(report, f, indent=4,sort_keys=True)
            print (f"Tier 1 audit report successfully written to {output_path}")
        except Exception as e:
            raise AuditError(f"Error writing audit.json: {e}", output_path.name)
    
    
        
def main():
    if len(sys.argv) != 3:
        print("usage: python pa2.py DEVICES.xml POLICY.yaml", file=sys.stderr)
        sys.exit(2)
        
    xml_file = sys.argv[1]
    yaml_file = sys.argv[2]
    
    try:
        auditor = FleetAuditor(xml_file,yaml_file)
        auditor.generate_report()
        
    except AuditError as e:
        filename_info =f" in '{e.filename}'" if e.filename else ""
        print(f"Error{filename_info}: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
        
         
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
    
    