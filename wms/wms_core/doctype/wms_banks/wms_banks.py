# Copyright (c) 2025, KNAPS and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class WMSBanks(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		account_number: DF.Data | None
		bank_name: DF.Link | None
		ifsc: DF.Data | None
		is_default: DF.Check
		parent: DF.Data
		parentfield: DF.Data
		parenttype: DF.Data
	# end: auto-generated types
	pass
