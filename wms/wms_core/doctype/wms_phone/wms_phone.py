# Copyright (c) 2025, KNAPS and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class WMSPhone(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		client: DF.Link
		is_primary_mobile_no: DF.Check
		is_primary_phone: DF.Check
		name: DF.Int | None
		phone: DF.Data
	# end: auto-generated types
	pass
