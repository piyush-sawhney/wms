# Copyright (c) 2025, KNAPS and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document


class WMSRDSchedule(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		from wms.wms_investment.doctype.wms_rd_transaction.wms_rd_transaction import WMSRDTransaction

		amended_from: DF.Link | None
		deposit_amount: DF.Float
		name: DF.Int | None
		rd_accounts: DF.Table[WMSRDTransaction]
		schedule_amount: DF.Float
		schedule_date: DF.Date | None
		schedule_document: DF.Attach | None
		schedule_number: DF.Data | None
		schedule_type: DF.Literal["Cash", "Cheque"]
		total_rebate: DF.Float
		total_surcharge: DF.Float
	# end: auto-generated types
	pass

	def before_validate(self):
		if self.is_new():
			self.schedule_number = None
			self.schedule_date = None
			self.total_rebate = None
			self.total_surcharge = None
			self.deposit_amount = None
			self.schedule_document = None

	def validate(self):
		self.validate_schedules()

	def before_save(self):
		self.validate_bank_account_number()

	def validate_bank_account_number(self):
		if self.schedule_type and self.schedule_type.lower() == "cheque":
			if self.rd_accounts:
				for row in self.rd_accounts:
					if not row.bank_account_number or len(row.bank_account_number) < 5:
						frappe.throw(_(f"Invalid bank account number for account {row.rd_account_number}."))

	def validate_schedules(self):
		if self.rd_accounts:
			account_list = []
			self.total_rebate = 0.0
			self.total_surcharge = 0.0
			self.schedule_amount = 0.0
			self.deposit_amount = 0.0
			for row in self.rd_accounts:
				if row.rd_account_number in account_list:
					frappe.throw(_(f"Duplicate Account Number: {row.rd_account_number}."))
				account_list.append(row.rd_account_number)
				if self.schedule_type and self.schedule_type.lower() == "cash":
					if row.cheque_number:
						frappe.throw(
							_(
								f"Cannot have cheque number for account {row.rd_account_number} in a cash schedule."
							)
						)
					row.bank_account_number = None
				elif self.schedule_type and self.schedule_type.lower() == "cheque":
					if not row.cheque_number or len(row.cheque_number) != 6:
						frappe.throw(_(f"Invalid cheque number for account {row.rd_account_number}."))

				else:
					frappe.throw(_("Invalid schedule type."))
				if row.denomination and row.number_of_installments:
					row.rd_amount = row.denomination * row.number_of_installments
					self.schedule_amount += row.rd_amount
					row.rd_deposit_amount = row.rd_amount
					if row.rebate:
						row.rd_deposit_amount -= row.rebate
						self.total_rebate += row.rebate
					if row.surcharge:
						row.rd_deposit_amount += row.surcharge
						self.total_surcharge += row.surcharge
					self.deposit_amount += row.rd_deposit_amount
