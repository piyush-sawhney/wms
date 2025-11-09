# Copyright (c) 2025, KNAPS and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class WMSRDAccount(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		account_number: DF.Data
		account_opening_date: DF.Date | None
		active: DF.Data | None
		amount: DF.Data | None
		bank_account_number: DF.Data | None
		card_number: DF.Data | None
		client_bank: DF.Link | None
		client_name: DF.Data | None
		default_installments: DF.Int
		denomination: DF.Float
		holder_name: DF.Data | None
		last_deposit_date: DF.Date | None
		last_updated: DF.Datetime | None
		new_card_number: DF.Data | None
		next_installment_date: DF.Date | None
		pending_installments: DF.Int
		po_investment: DF.Link
		rebate: DF.Float
		start_date: DF.Data | None
		surcharge: DF.Float
		total_deposit_amount: DF.Float
		total_month_paid: DF.Int
	# end: auto-generated types
	pass
