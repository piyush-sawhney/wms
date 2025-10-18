# Copyright (c) 2025, KNAPS and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class WMSPhoneNumber(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		is_primary_phone: DF.Check
		is_whatsapp_number: DF.Check
		parent: DF.Data
		parentfield: DF.Data
		parenttype: DF.Data
		phone: DF.Phone | None
	# end: auto-generated types
	pass
