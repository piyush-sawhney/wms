# Copyright (c) 2025, KNAPS and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import re

class WMSClient(Document):
	def validate(self):
		self.validate_pan()
		self.validate_client_name()
		self.validate_client_type()
		self.validate_classification()	

	def validate_client_name(self):
		if not self.client_name:
			frappe.throw("Client Name is mandatory")
		if len(self.client_name) < 3:
			frappe.throw("Client Name must be at least 3 characters long")

	def validate_client_type(self):
		if not self.type:
			frappe.throw("Client Type is mandatory")
		valid_types = [
			"Individual", "Body of Individuals (BOI)", "Association of Persons (AOP)",
			"Hindu Undivided Family (HUF)", "Company", "Limited Liability Partnership (LLP)",
			"Partnership Firm", "Trust", "Government Agency", "Local Authority", "Artificial Judicial Person"
		]
		if self.type not in valid_types:
			frappe.throw(f"Invalid Client Type. Must be one of: {', '.join(valid_types)}")

	def validate_classification(self):
		if not self.classification:
			frappe.throw("Client Classification is mandatory")


	def validate_pan(self):
		if not self.pan:
			return
		self.pan = self.pan.strip().upper()
		if len(self.pan) != 10:
			frappe.throw("PAN must be 10 characters long")
		if not self.pan.isalnum():
			frappe.throw("PAN must be alphanumeric")
		pan_pattern = r'^[A-Z]{5}[0-9]{4}[A-Z]$'
		
		if not re.match(pan_pattern, self.pan):
			frappe.throw("Invalid PAN format. It should be like 'ABCDE1234F'.")
		self.validate_pan_type()
		
	def validate_pan_type(self):
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
	def validate_resident_details(self):
		pass  # Placeholder for future individual-specific validations	
	def validate_minor_details(self):
		pass	# Placeholder for future minor-specific validations
	def validate_non_resident_details(self):
		pass  # Placeholder for future non-resident-specific validations
	def validate_sole_propritor_details(self):
		pass	# Placeholder for future sole proprietor-specific validations
	def validate_huf_details(self):
		pass	
