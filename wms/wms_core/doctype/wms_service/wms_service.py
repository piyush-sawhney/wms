# Copyright (c) 2025, KNAPS and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class WMSService(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		description: DF.SmallText | None
		entry_date: DF.Date
		notes: DF.TextEditor | None
		service_for: DF.Link
		service_link: DF.DynamicLink | None
		status: DF.Literal["Entry Done", "Submitted to PO", "Client Dependency", "Pending With Us", "Resolved", "Rejected"]
		type: DF.Link
	# end: auto-generated types
	pass
