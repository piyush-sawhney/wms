# Copyright (c) 2025, KNAPS and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import re

class WMSClient(Document):
    def validate(self):
        self.validate_pan()
    
    
    def validate_pan(self):
        if not self.pan or not self.type:
            return  # Skip validation if either field is missing

        # Convert PAN to uppercase for consistency
        self.pan = self.pan.upper()

        # PAN format: 5 letters, 4 digits, 1 letter
        pan_pattern = r'^[A-Z]{5}[0-9]{4}[A-Z]$'
        if not re.match(pan_pattern, self.pan):
            frappe.throw("Invalid PAN format. It should be like 'ABCDE1234F'.")

        # Type to PAN 4th character mapping
        type_to_pan_code = {
            "Individual": "P",
            "Body of Individuals (BOI)": "B",
            "Association of Persons (AOP)": "A",
            "Hindu Undivided Family (HUF)": "H",
            "Company": "C",
            "Limited Liability Partnership (LLP)": "E",
            "Partnership Firm": "F",
            "Trust": "T",
            "Government Agency": "G",
            "Local Authority": "L",
            "Artificial Judicial Person": "J"
        }
        expected_code = type_to_pan_code.get(self.type)
        actual_code = self.pan[3]

        if expected_code and actual_code != expected_code:
            frappe.throw(
                f"PAN does not match the selected type '{self.type}'. "
                f"The 4th character should be '{expected_code}', but found '{actual_code}'."
            )