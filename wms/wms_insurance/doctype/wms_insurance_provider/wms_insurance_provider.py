# Copyright (c) 2025, KNAPS and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class WMSInsuranceProvider(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		provider_name: DF.Data
	# end: auto-generated types
	
	def autoname(self):
		"""
		Generate a unique name for the insurance provider if not already set.
		The name is generated based on the provider's name.
		"""
		self.provider_name = self.provider_name.strip().title()  # Remove unsafe chars and format name
		self.name = self.provider_name
