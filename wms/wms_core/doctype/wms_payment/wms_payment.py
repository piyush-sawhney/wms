# Copyright (c) 2025, KNAPS and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class WMSPayment(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		account_number: DF.Data | None
		amount: DF.Currency
		bank: DF.Link | None
		currency: DF.Link | None
		name: DF.Int | None
		number: DF.Data | None
		payment_date: DF.Date | None
		type: DF.Link
	# end: auto-generated types
	pass
