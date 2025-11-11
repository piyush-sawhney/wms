# Copyright (c) 2025, KNAPS and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document


class WMSRDAccount(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		account_number: DF.Data | None
		account_opening_date: DF.Date | None
		active: DF.Data | None
		amount: DF.Currency
		bank_account_number: DF.Data | None
		card_number: DF.Data | None
		client_bank: DF.Link | None
		client_name: DF.Data | None
		default_installments: DF.Float
		denomination: DF.Float
		holder_name: DF.Data | None
		is_card_updated: DF.Check
		last_deposit_date: DF.Date | None
		last_updated: DF.Datetime | None
		new_card_number: DF.Data | None
		next_installment_date: DF.Date | None
		pending_installments: DF.Float
		po_investment: DF.Link | None
		rd_account_number: DF.Data | None
		rebate: DF.Float
		start_date: DF.Date | None
		surcharge: DF.Float
		total_deposit_amount: DF.Float
		total_month_paid: DF.Int
	# end: auto-generated types
	pass

	def before_save(self):
		self.validate_account_numbers()
		self.validate_denomination()
		self.validate_start_date()

	def validate_start_date(self):
		if self.po_investment and not self.start_date:
			frappe.throw(_("Start date cannot be empty"))
		if self.start_date:
			if str(self.start_date) != self.account_opening_date:
				frappe.throw(_("Start date mismatch."))

	def validate_denomination(self):
		if self.amount:
			if float(self.amount) != float(self.denomination):
				frappe.throw(_("Denomination mismatch."))

	def validate_account_numbers(self):
		if self.account_number:
			if self.account_number != self.rd_account_number:
				frappe.throw(_("Account number mismatch."))
