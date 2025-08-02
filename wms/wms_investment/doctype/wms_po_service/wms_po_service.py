# Copyright (c) 2025, KNAPS and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document
from frappe.model.naming import make_autoname


class WMSPOService(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		description: DF.SmallText | None
		entry_date: DF.Date
		investment: DF.Link
		status: DF.Literal["Entry Done"]
		type: DF.Link
	# end: auto-generated types
	pass


	def autoname(self):
		self.name = make_autoname(f"{self.investment}-.###")
