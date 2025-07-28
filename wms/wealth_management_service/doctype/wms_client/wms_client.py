# Copyright (c) 2025, KNAPS and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class WMSClient(Document):
	def validate(self):
		self.validate_pan_type_combination()
		self.validate_client_name()

	def validate_client_name(self):
		if not self.client_name:
			frappe.throw("Client Name is mandatory")
		if len(self.client_name) < 3:
			frappe.throw("Client Name must be at least 3 characters long")
		
	def validate_pan_type_combination(self):
		if not self.pan:
			return
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
