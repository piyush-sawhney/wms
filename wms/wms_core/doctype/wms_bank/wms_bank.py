# Copyright (c) 2025, KNAPS and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe import _

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
		client_name: DF.Data | None
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
		self.validate_account_number()

	def validate_account_number(self):
		if self.bank_name:
			if "post office" not in self.bank_name.lower():
				if self.account_number and len(self.account_number) > 4:
					frappe.throw(_("Enter only last 4 digits of account number for accounts other than Post Office."))
			else:
				if frappe.db.exists("WMS Bank", {"account_number": self.account_number, "name": ["!=", self.name]}):
					frappe.throw(_("Account number must be unique."))

	def validate_bank_name(self):
		if not self.bank_name:
			frappe.throw(_("Bank Name is required."))
		if len(self.bank_name) < 3:
			frappe.throw(_("Bank Name must be at least 3 characters long."))

	def validate_ifsc(self):
		if self.ifsc:
			self.ifsc = self.ifsc.replace(" ", "")
			if len(self.ifsc) != 11:
				frappe.throw(_("IFSC code must be exactly 11 characters long."))
			if not self.ifsc.isalnum():
				frappe.throw(_("IFSC code must contain only alphanumeric characters."))

	def format_fields(self):
		self.bank_name = self.bank_name.strip().upper()
		if self.ifsc:
			self.ifsc = self.ifsc.upper()
		if self.branch:
			self.branch = self.branch.strip().title()

	def validate_micr(self):
		if self.micr:
			self.micr = self.micr.replace(" ", "")
			if len(self.micr) != 9:
				frappe.throw(_("MICR code must be exactly 9 digits long."))
			if not self.micr.isdigit():
				frappe.throw(_("MICR code must contain only digits."))
