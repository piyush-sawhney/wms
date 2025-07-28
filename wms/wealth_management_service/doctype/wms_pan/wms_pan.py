# Copyright (c) 2025, KNAPS and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import re
class WMSPAN(Document):
	def validate(self):
		self.validate_pan()

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
