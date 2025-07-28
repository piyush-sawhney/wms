# Copyright (c) 2025, KNAPS and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class WMSClient(Document):
	def before_save(self):
		self.update_classification_for_individuals()
		
	def validate(self):
		self.validate_client_name()

	def validate_client_name(self):
		if not self.client_name:
			frappe.throw("Client Name is mandatory")
		if len(self.client_name) < 3:
			frappe.throw("Client Name must be at least 3 characters long")
		
	def update_classification_for_individuals(self):
		if self.dob and self.type == "Individual" and self.classification != "Sole Proprietor":
			age = calculate_age(self.dob)
			if age < 18:
				if self.classification != "Minor":
					self.classification = "Minor"
					frappe.msgprint("Classification updated to Minor based on age.")
			elif age >= 18 and self.classification == "Minor":
				frappe.throw("Minor cannot be greater than 18 years old. ")

	def validate_non_resident_details(self):
		pass  # Placeholder for future non-resident-specific validations
	def validate_sole_propritor_details(self):
		pass	# Placeholder for future sole proprietor-specific validations
	def validate_huf_details(self):
		pass	

def calculate_age(dob):
	dob_date = frappe.utils.getdate(dob)
	today = frappe.utils.nowdate()
	return frappe.utils.date_diff(today, dob_date) // 365
