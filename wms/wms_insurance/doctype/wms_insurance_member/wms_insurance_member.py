# Copyright (c) 2025, KNAPS and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class WMSInsuranceMember(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		member_name: DF.Link
		parent: DF.Data
		parentfield: DF.Data
		parenttype: DF.Data
		sum_assured: DF.Float
	# end: auto-generated types
	pass
