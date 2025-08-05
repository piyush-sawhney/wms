# Copyright (c) 2025, KNAPS and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import re
class WMSPAN(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		pan: DF.Data | None
	# end: auto-generated types
	def autoname(self):
			self.name = self.pan.strip().upper()

	def validate(self):
		self.validate_pan()

	def validate_pan(self):
		if not self.pan:
			return
		if len(self.pan) != 10:
			frappe.throw("PAN must be 10 characters long")
		if not self.pan.isalnum():
			frappe.throw("PAN must be alphanumeric")
		pan_pattern = r'^[A-Z]{5}[0-9]{4}[A-Z]$'
		
		if not re.match(pan_pattern, self.pan):
			frappe.throw("Invalid PAN format. It should be like 'ABCDE1234F'.")
