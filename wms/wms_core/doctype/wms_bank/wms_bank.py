# Copyright (c) 2025, KNAPS and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class WMSBank(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		account_number: DF.Data
		bank_name: DF.Data
		branch: DF.Data | None
		client: DF.Link
		ifsc: DF.Data | None
		micr: DF.Data | None
		name: DF.Int | None
		type: DF.Literal["Savings", "Current", "NRE", "NRO", "FCNR"]
	# end: auto-generated types
	def before_save(self):
		self.format_fields()
	
	def validate(self):
		self.validate_micr()
		self.validate_ifsc()
		self.validate_bank_name()
	
	def validate_bank_name(self):
		if not self.bank_name:
			frappe.throw("Bank Name is required.")
		if len(self.bank_name) < 3:
			frappe.throw("Bank Name must be at least 3 characters long.")

	def validate_ifsc(self):
		if self.ifsc:
			self.ifsc = self.ifsc.replace(" ", "")
			if len(self.ifsc) != 11:
				frappe.throw("IFSC code must be exactly 11 characters long.")
			if not self.ifsc.isalnum():
				frappe.throw("IFSC code must contain only alphanumeric characters.")

	def format_fields(self):
		self.bank_name = self.bank_name.strip().title()
		if self.ifsc:
			self.ifsc = self.ifsc.upper()
		if self.branch:
			self.branch = self.branch.strip().title()
		
		
	def validate_micr(self):
		if self.micr:
			self.micr = self.micr.replace(" ", "")
			if len(self.micr) != 9:
				frappe.throw("MICR code must be exactly 9 digits long.")
			if not self.micr.isdigit():
				frappe.throw("MICR code must contain only digits.")