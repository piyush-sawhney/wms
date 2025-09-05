# Copyright (c) 2025, KNAPS and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class WMSPOScheme(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		code: DF.Data
		period: DF.Int
		roi: DF.Float
		scheme_name: DF.Data
	# end: auto-generated types

	def autoname(self):
		roi_formatted = f"{self.roi:.2f}".replace(".", "-")
		self.name = f"{self.code.upper()}-{self.period}M-R{roi_formatted}"

	def validate(self):
		self.validate_scheme()

	def validate_scheme(self):
		if not self.code:
			frappe.throw("Code is required for the scheme.")
		if not self.period:
			frappe.throw("Period is required for the scheme.")
		if not self.roi:
			frappe.throw("ROI is required for the scheme.")
		if not self.scheme_name:
			frappe.throw("Scheme Name is required for the scheme.")
		self.scheme_name = self.scheme_name.title().strip()
		self.code = self.code.upper().strip()
