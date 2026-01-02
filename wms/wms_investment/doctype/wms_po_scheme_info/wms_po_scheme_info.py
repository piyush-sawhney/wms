# Copyright (c) 2026, KNAPS and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class WMSPOSchemeInfo(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		scheme_code: DF.Data | None
		scheme_name: DF.Data | None
	# end: auto-generated types
	pass

	def before_naming(self):
		self.scheme_code = self.scheme_code.strip().upper() if self.scheme_code else self.scheme_code
		
	def before_validate(self):
		self.scheme_name = self.scheme_name.strip().title() if self.scheme_name else self.scheme_name