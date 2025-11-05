# Copyright (c) 2025, KNAPS and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class WMSPOExtension(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		extension_date: DF.Date
		extension_period: DF.Int
		parent: DF.Data
		parentfield: DF.Data
		parenttype: DF.Data
		scheme_roi: DF.Float
	# end: auto-generated types
	pass
