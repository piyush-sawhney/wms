# Copyright (c) 2025, KNAPS and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import re

class WMSClient(Document):
    def validate(self):
        self.validate_pan()
        self.validate_dob()
        self.validate_minor()
        self.validate_contact() 
        self.validate_full_name()
        self.validate_pob()
        self.validate_karta_details()   
    
    def before_save(self):
        # Ensure that the full_name is stripped of leading and trailing spaces
        if self.full_name:
            self.full_name = self.full_name.strip()
        
        # Ensure that the place of birth is stripped of leading and trailing spaces
        if self.pob:
            self.pob = self.pob.strip()
      
    
    def validate_full_name(self):
        if not self.full_name:
            frappe.throw("Name cannot be empty.")
        if not isinstance(self.full_name, str):
            frappe.throw("Name must be a string.")
    
    def validate_pob(self):
        if not self.pob:
            return  # Skip validation if place of birth is not provided
        if not isinstance(self.pob, str):
            frappe.throw("Place of Birth must be a string.")
    
    def validate_minor(self):
        if self.dob and self.type == "Individual":
            dob_date = frappe.utils.getdate(self.dob)
            today = frappe.utils.nowdate()
            age = frappe.utils.date_diff(today, dob_date) // 365
            if self.sub_type == "Minor":
                if age > 18:
                    frappe.throw("Minor clients must be under 18 years old. Please check the date of birth.")
            else:
                if age < 18:
                    frappe.throw("Age is less than 18, please select Minor")


        
    def validate_contact(self):
        if not self.contact and self.type == "Individual":
            frappe.throw("Contact field cannot be empty for the an Individual.")

    def validate_karta_details(self):
        if self.type == "Hindu Undivided Family (HUF)" and not self.karta_details:
            frappe.throw("Karta is required for HUF clients.")
              
    def validate_dob(self):
        if not self.dob:
            return
        # Ensure dob is a valid date
        if not isinstance(self.dob, str):
            frappe.throw("DOB must be a valid date string.")
        try:
            frappe.utils.getdate(self.dob)
        except ValueError:
            frappe.throw("Invalid date format for DOB. Please use YYYY-MM-DD format.")           
    
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