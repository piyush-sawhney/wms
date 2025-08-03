# Copyright (c) 2025, KNAPS and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class WMSMFScheme(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		amc: DF.Link
		option: DF.Literal["IDCW", "Growth", "Bonus"]
		plan: DF.Literal["Regular", "Direct"]
		scheme_name: DF.Data
	# end: auto-generated types
	pass
