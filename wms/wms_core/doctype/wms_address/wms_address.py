# Copyright (c) 2025, KNAPS and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class WMSAddress(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		address_1: DF.Data | None
		address_2: DF.Data | None
		address_3: DF.Data | None
		city: DF.Data | None
		client: DF.Link
		country: DF.Link | None
		district: DF.Data | None
		name: DF.Int | None
		pincode: DF.Data | None
		state: DF.Data | None
		type: DF.Literal["Home", "Work", "Others"]
	# end: auto-generated types
	pass
